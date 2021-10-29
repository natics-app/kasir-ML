const chrome = require('selenium-webdriver/chrome');
const {Builder, By, until} = require('selenium-webdriver');
const { Readability } = require("@mozilla/readability");
const jsdom = require('jsdom');
const { JSDOM } = jsdom;
const fs = require('fs');
const csv = require('fast-csv');
const ws = fs.createWriteStream(__dirname + "/data.csv");
const axios = require('axios');

let driver = new Builder()
    .forBrowser('chrome')
    .setChromeOptions(new chrome.Options().headless())
    .build();

let newsLink = [];
let articles = [];

async function parse(url, index, trial) {
    process.stdout.write(`Processing [${index+1}/${newsLink.length}]: ${url}`);

    try {
        let virtualConsole = new jsdom.VirtualConsole();
        let doc = await JSDOM.fromURL(url, { virtualConsole });

        const reader = new Readability(doc.window.document);
        let article = reader.parse();
        article["url"] = url;
        articles.push(article);

        process.stdout.write(`\rProcessed [${index+1}/${newsLink.length}]: ${url} ✅\n`);
    } catch(e) {
        // process.stdout.write(`\rFailed to process [${trial}] ${url} ❌\n`);
        process.stdout.write(`\n(${trial}) ${e.toString()}\n`);
        
        if (trial < 3) {
            await parse(url, index, trial + 1);
        }
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

        let news = await driver.findElements(By.css("#rso a"));

        for (let berita of news) {
            let link = await berita.getAttribute("href");
            newsLink.push(link);
            console.log(link);
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
    let keywords = await getKeywords();
    for (let query of keywords) {
        console.log(query);
        for (let i = 0; i <= 30; i += 10) {
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