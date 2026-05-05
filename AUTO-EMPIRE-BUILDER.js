// 🔥 AUTO-EMPIRE-BUILDER.JS - Self-Deploying 49-File Site
// Upload → Auto-generates everything → Live in 90 seconds
// Benny "Palmo Kid" - Zero terminal required

const fs = require('fs');

// CONFIG
const AFF_ID = '2013017799';
const SITE_URL = 'https://brightlane.github.io/FlowerDelivery/';

// AUTO-GENERATE 49 FILES
console.log('🔥 AUTO-BUILDING 49 FILES...');

const occasions = ['mothers-day', 'birthday', 'sympathy', 'anniversary', 'romance'];
occasions.forEach(occ => {
  const filename = `${occ}-flowers.html`;
  const content = `<!DOCTYPE html>
<html><head><title>${occ} Flowers | Same-Day Delivery</title></head>
<body>
<h1>${occ.toUpperCase()} FLOWERS</h1>
<a href="https://www.floristone.com/main.cfm?occ=${occ}&source_id=aff&affid=${AFF_ID}" 
style
