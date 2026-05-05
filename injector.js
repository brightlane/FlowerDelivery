// injector.js - Injects high-converting affiliate elements
const fs = require('fs-extra');
const path = require('path');
const cheerio = require('cheerio');

class AffiliateInjector {
  constructor() {
    this.inputDir = 'generated-pages/';
    this.outputDir = 'optimized-pages/';
    this.ctaTemplates = [
      '<div class="cta-primary"><a href="{AFFILIATE_URL}" rel="sponsored">Order Now - {DISCOUNT}% Off {CITY} Delivery</a></div>',
      '<div class="cta-urgency">Limited Stock! Same Day {KEYWORD} {CITY} <a href="{AFFILIATE_URL}">Shop Now</a></div>'
    ];
  }

  async injectAll() {
    console.log('💉 Injecting affiliate optimizations...');
    
    await fs.ensureDir(this.outputDir);
    
    const files = await fs.readdir(this.inputDir);
    
    for (const file of files) {
      if (!file.endsWith('.html')) continue;
      
      const inputPath = path.join(this.inputDir, file);
      const outputPath = path.join(this.outputDir, file);
      
      const content = await fs.readFile(inputPath, 'utf8');
      const optimized = this.injectPage(content, file);
      
      await fs.writeFile(outputPath, optimized);
      process.stdout.write(`\r💰 Optimized ${files.indexOf(file) + 1}/${files.length}`);
    }
    
    console.log(`\n✅ ${files.length} money pages optimized!`);
  }

  injectPage(html, filename) {
    const $ = cheerio.load(html);
    
    // Extract keyword/city from filename
    const match = filename.match(/([a-z-]+)-([a-z-]+)/);
    const keyword = match?.[1]?.replace(/-/g, ' ') || 'flowers';
    const city = match?.[2]?.replace(/-/g, ' ') || 'local';
    
    // 1. Inject hero CTA above fold
    $('h1').after(this.getHeroCTA(keyword, city));
    
    // 2. Inject affiliate comparison table
    $('main').prepend(this.getComparisonTable());
    
    // 3. Add exit-intent popup code
    $('body').append(this.getExitIntentScript(city));
    
    // 4. Optimize images with lazy loading
    $('img').attr('loading', 'lazy');
    
    // 5. Add tracking pixels
    $('head').append('<script async src="analytics.js"></script>');
    
    return $.html();
  }

  getHeroCTA(keyword, city) {
    const discount = Math.floor(Math.random() * 20) + 10;
    return `<div class="hero-cta" style="background: #ff6b6b; color: white; padding: 20px; text-align: center; margin: 20px 0;">
      🚨 ${discount}% OFF First Order! Same Day ${keyword} ${city} Delivery
      <br><a href="/go/1800flowers?kw=${keyword}&city=${city}" style="background: #fff; color: #ff6b6b; padding: 15px 30px; text-decoration: none; font-weight: bold; border-radius: 5px; display: inline-block; margin-top: 10px;" rel="sponsored">Order Now - Guaranteed Delivery</a>
    </div>`;
  }

  getComparisonTable() {
    return `<table class="affiliate-comparison" style="width: 100%; border-collapse: collapse; margin: 20px 0;">
      <thead>
        <tr><th>Florist</th><th>${city} Delivery</th><th>Price</th><th>Rating</th></tr>
      </thead>
      <tbody>
        <tr>
          <td>1800Flowers</td>
          <td>Same Day</td>
          <td>$49.99</td>
          <td>4.8⭐</td>
        </tr>
        <tr style="background: #f0f8ff;">
          <td><strong>BEST DEAL →</strong></td>
          <td>1hr Delivery</td>
          <td>$39.99</td>
          <td>4.9⭐</td>
          <td><a href="/go/bestdeal?city=${city}" rel="sponsored" style="background: green; color: white; padding: 8px 16px;">Order Now</a></td>
        </tr>
      </tbody>
    </table>`;
  }

  getExitIntentScript(city) {
    return `<script>
      let exitIntentShown = false;
      document.addEventListener('mouseleave', function(e) {
        if (!exitIntentShown && e.clientY < 0) {
          // Exit intent popup
          const popup = document.createElement('div');
          popup.innerHTML = 'Wait! Get 20% OFF ${city} flowers before you go! <a href="/go/special?city=${city}" rel="sponsored">Claim Deal</a>';
          popup.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.8);color:white;z-index:9999;display:flex;align-items:center;justify-content:center;font-size:24px;';
          document.body.appendChild(popup);
          exitIntentShown = true;
          setTimeout(() => popup.remove(), 5000);
        }
      });
    </script>`;
  }
}

(async () => {
  const injector = new AffiliateInjector();
  await injector.injectAll();
})();
