const express = require("express");
const path = require("path");
const fs = require("fs");
const os = require("os");
const childProcess = require("child_process");

const app = express();
const port = 3000;

app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(express.static(path.join(__dirname, "..", 'dist')));

app.post("/api/actions/command", (req, res) => {
    const filename = `isl-${Date.now()}.json`;
    const tmpPath = path.join(os.tmpdir(), filename);
    fs.writeFileSync(tmpPath, JSON.stringify(req.body.isl), {encoding: "utf8"});

        const args = String(req.body.command).replace("$ISLJSON", tmpPath).split(/\s+/);
        const command = args.shift()

        console.log(`running command: ${command} ${args}`);
        const proc = childProcess.spawn(command, args, {cwd: path.join(__dirname, "..", "..")});
        console.log(`PID = ${proc.pid}`);

        proc.stdout.on("data", data => {
            console.log(`${proc.pid}> ${data}`);
        });
        proc.stderr.on("data", data => {
            console.log(`${proc.pid}> ${data}`);
        });
        proc.on('close', (code) => {
            console.log(`${proc.pid}> child process exited with code ${code}`);
        });
        proc.on('error', err => {
            console.log(`${proc.pid}> ${err}`);
        });
});

app.listen(port, () => {
    console.log(`Please open http://localhost:${port}/`);
});
