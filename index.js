const chrome = require('selenium-webdriver/chrome');
const {Builder, By, until} = require('selenium-webdriver');
const { Readability } = require("@mozilla/readability");
const jsdom = require('jsdom');
const { JSDOM } = jsdom;
const fs = require('fs');
const csv = require('fast-csv');
const ws = fs.createWriteStream(__dirname + "/data.csv");
const axios = require('axios');
const Timeout = require('await-timeout');

let driver = new Builder()
    .forBrowser('chrome')
    .setChromeOptions(new chrome.Options().headless())
    .build();

let newsLink = [];
let articles = [];

async function fetchJSDOM(url, virtualConsole) {
    const promise = JSDOM.fromURL(url, { virtualConsole });
    return Timeout.wrap(promise, 5000, "Timeout");
}

async function parse(news, index, trial) {
    process.stdout.write(`Processing [${index+1}/${newsLink.length}]: ${news.url}`);

    try {
        let virtualConsole = new jsdom.VirtualConsole();
        let doc = await fetchJSDOM(news.url, virtualConsole);

        const reader = new Readability(doc.window.document);
        let article = reader.parse();
        article["url"] = news.url;
        article["date"] = news.date;
        articles.push(article);

        process.stdout.write(`\rProcessed [${index+1}/${newsLink.length}]: ${news.url} ✅\n`);
    } catch(e) {
        // process.stdout.write(`\rFailed to process [${trial}] ${news.url} ❌\n`);
        process.stdout.write(`\n(${trial}) ${e.toString()}\n`);
        
        if (trial < 3) {
            await parse(news, index, trial + 1);
        }
    }
}

async function checkUrl(url) {
    try {
        const response = await axios.get('https://kasir.farrelanshary.me/api/general/check-url', {
            params: {
                api_key: "bukanUser",
                url: url
            }
        });
        return response.data.data.is_existing
    }
    catch (error) {
        console.error(error);
    }

}

async function crawler(index, searchString) {
    let params = {
        q: searchString,
        tbm: "nws",
        start: index
    }

    let urlParams = new URLSearchParams(params).toString();
    
    await driver.get('https://google.com/search?' + urlParams);
    try {
        await driver.wait(until.elementLocated(By.id("rso")), 5000);

        const news = await driver.findElements(By.css("#rso a"));

        for (const singleNews of news) {
            const link = await singleNews.getAttribute("href");
            const tanggal = await singleNews.findElement(By.css('p.S1FAPd.OSrXXb.ecEXdc span')).getText();

            const existing = await checkUrl(link);

            if (!existing) {
                newsLink.push({
                    "url": link,
                    "news_date": tanggal
                });
                console.log(link);
            }
            else {
                console.log('Skipped ' + link);
            }
        }
    } catch {
        console.log("Timed out or blocked by captcha");
        driver.quit();
        process.exit();
    }
}

async function getKeywords() {
    try {
        const response = await axios.get('https://kasir.farrelanshary.me/api/general/keywords', {
            params: {
                api_key: "bukanUser"
            }
        });
        return response.data.data.keywords;
    } catch (error) {
        console.error(error);
    }
}

async function main() {
    let keywords = ["penyelundupan hewan", "penyitaan hewan", "perburuan hewan", "perdagangan hewan"];
    for (let query of keywords) {
        console.log(query);
        for (let i = 0; i <= 40; i += 10) {
            await crawler(i, query);
        }
    }

    driver.quit();

    for (let [i, link] of newsLink.entries()) {
        await parse(link, i, 1);
    }

    csv
        .write(articles, { headers: true })
        .pipe(ws);

    console.log("Done");
}

main();