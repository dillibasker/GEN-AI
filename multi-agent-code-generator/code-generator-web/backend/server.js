const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors());
app.use(express.json());

app.post('/api/generate', (req, res) => {
  const { requirement, language } = req.body;

  if (!requirement || !language) {
    return res.status(400).json({ error: 'Requirement and language are required' });
  }

  // Adjust path if needed
const pythonScript = path.join(__dirname, 'main.py');
 //for local
/*const python = spawn(
  'C:/Users/Dell/OneDrive/Desktop/My_Project/Gen-AI/Langchain/multi-agent-code-generator/venv310/Scripts/python.exe',
  [pythonScript],
  { cwd: path.dirname(pythonScript) }
);*/

//for production 
const pythonPath = process.env.PYTHON_PATH || 'python';

const python = spawn(pythonPath, [pythonScript], {
  cwd: path.dirname(pythonScript)
});

  let dataBuffer = '';
  let errorOutput = '';

  // Send inputs
  python.stdin.write(requirement + '\n');
  python.stdin.write(language + '\n');
  python.stdin.end();

  python.stdout.on('data', (data) => {
    dataBuffer += data.toString();
  });

  python.stderr.on('data', (data) => {
    errorOutput += data.toString();
  });

  python.on('close', (code) => {
    console.log("Exit Code:", code);

    if (code !== 0) {
      console.error("Python Error:", errorOutput);
      return res.status(500).json({
        error: 'Python script failed',
        details: errorOutput
      });
    }

    const result = parseOutput(dataBuffer);
    res.json(result);
  });
});

function parseOutput(output) {
  const sections = {
    plan: '',
    design: '',
    code: '',
    test_result: '',
    summary: '',
    raw: output
  };

  try {
    const planMatch = output.match(/--- PLAN ---\s*([\s\S]*?)(?=\n--- DESIGN ---|$)/);
    const designMatch = output.match(/--- DESIGN ---\s*([\s\S]*?)(?=\n--- GENERATED CODE ---|$)/);
    const codeMatch = output.match(/--- GENERATED CODE ---\s*([\s\S]*?)(?=\n--- TEST RESULT ---|$)/);
    const testMatch = output.match(/--- TEST RESULT ---\s*([\s\S]*?)(?=\n--- SUMMARY ---|$)/);
    const summaryMatch = output.match(/--- SUMMARY ---\s*([\s\S]*?)$/);

    if (planMatch) sections.plan = planMatch[1].trim();
    if (designMatch) sections.design = designMatch[1].trim();
    if (codeMatch) sections.code = codeMatch[1].trim();
    if (testMatch) sections.test_result = testMatch[1].trim();
    if (summaryMatch) sections.summary = summaryMatch[1].trim();

  } catch (e) {
    console.error('Parse error:', e);
  }

  return sections;
}

app.listen(PORT, () => {
  console.log(`Backend server running on port ${PORT}`);
});