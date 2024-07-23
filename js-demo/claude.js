const { ChatAnthropic } = require("@langchain/anthropic");


async function main() {
    const model = new ChatAnthropic({
        temperature: 0.9,
        model: "claude-3-5-sonnet-20240620",
        apiKey: process.env.ANTHROPIC_API_KEY,
        //   maxTokens: 1024,
    });

    let output;
    try {
        const res = await model.invoke("Why is the sky blue?");
        output = res.content;
    } catch (err) {
        console.error('invoke failed', err);
    }

    console.log(output);
}

main();