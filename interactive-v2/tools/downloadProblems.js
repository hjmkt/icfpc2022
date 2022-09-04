const fs = require("fs");
const path = require("path");
const axios = require("axios");
const maxProblems = 40;

async function main() {
    for (let i = 1; i <= maxProblems; i++) {
        await axios
            .get(`https://cdn.robovinci.xyz/imageframes/${i}.json`)
            .then((response) => {
                // console.log(response);
                console.log(`${i}.json`);
                fs.writeFileSync(
                    path.join("static", `${i}.json`),
                    JSON.stringify(response.data),
                    { encoding: "utf-8" }
                );
            });

        if (i >= 26) {
            await axios
                .get(`https://cdn.robovinci.xyz/imageframes/${i}.initial.json`)
                .then((response) => {
                    // console.log(response);
                    console.log(`${i}.initial.json`);
                    fs.writeFileSync(
                        path.join("static", `${i}.initial.json`),
                        JSON.stringify(response.data),
                        { encoding: "utf-8" }
                    );
                });
        }

        if (i >= 36) {
            await axios
                .get(`https://cdn.robovinci.xyz/sourcepngs/${i}.source.json`)
                .then((response) => {
                    // console.log(response);
                    console.log(`${i}.source.json`);
                    fs.writeFileSync(
                        path.join("static", `${i}.source.json`),
                        JSON.stringify(response.data),
                        { encoding: "utf-8" }
                    );
                });
        }
    }
}

main().catch(console.error.bind(console));
