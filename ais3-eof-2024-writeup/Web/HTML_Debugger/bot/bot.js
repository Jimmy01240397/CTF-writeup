const puppeteer = require('puppeteer')

const DOMAIN = process.env.DOMAIN || 'web'
const FLAG = process.env.FLAG || 'FL4G{fake}'

const sleep = async ms => new Promise(resolve => setTimeout(resolve, ms))

let browser = null

const visit = async url => {
    let context = null
    try {
        if (!browser) {
            const args = ['--js-flags=--jitless,--no-expose-wasm', '--disable-gpu', '--disable-dev-shm-usage']
            browser = await puppeteer.launch({
                headless: 'new',
                args
            })
        }

        context = await browser.createIncognitoBrowserContext()
        const page = await context.newPage()

        await page.setCookie({name: 'flag', value: FLAG, domain: DOMAIN});

        await page.goto(url)
        await page.bringToFront()
        await sleep(3000)
        await page.click('#close_btn')
        await sleep(2000)
        await page.close()

        await context.close()
        context = null
    } catch (e) {
        console.log(e)
    } finally {
        if (context) await context.close()
    }
}

module.exports = visit

if (require.main === module) {
    visit('http://example.com')
}
