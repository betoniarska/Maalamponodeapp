const express = require('express');
const bodyParser = require('body-parser');
const { spawn } = require('child_process');
const path = require('path');

const app = express();
const port = 3001;



app.use(bodyParser.json());

app.use(express.static(path.join(__dirname, 'public')));

app.post('/process-data', (req, res) => {
    const data = req.body;

    const pythonProcess = spawn('python', [path.join(__dirname, 'script.py'), JSON.stringify(data)]);

    let pythonOutput = '';

    pythonProcess.stdout.on('data', (data) => {
        pythonOutput += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`stderr: ${data}`);
    });

    pythonProcess.on('close', (code) => {
        if (code !== 0) {
            return res.status(500).send('Error processing data');
        }
        try {
            const result = JSON.parse(pythonOutput);
            res.json(result);
        } catch (e) {
            res.status(500).send('Error parsing Python script output');
        }
    });
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}/`);
});