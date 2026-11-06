"use strict";
const test=require("node:test");
const assert=require("node:assert/strict");
const fs=require("node:fs");
const path=require("node:path");
const root=path.resolve(__dirname,"..");
const read=p=>fs.readFileSync(path.join(root,p),"utf8");
test("Privacy disclosures cover Google vendors, third-party cookies, advertising opt-outs and CMP obligations",()=>{
 const s=read("privacy.html");
 for(const literal of ["Third-party vendors, including Google","cookies","web beacons","IP addresses","myadcenter.google.com","optout.aboutads.info","European Economic Area","certified consent management platform","support@printerresolve.com"]){
  assert.ok(s.includes(literal),"Missing privacy disclosure: "+literal);
 }
 assert.ok(!s.includes("we use a certified consent management platform"),"Do not claim unverified CMP setup");
});
test("Four strengthened articles include genuinely distinct worked evidence, not cosmetic copy",()=>{
 const markers=[
 ["printer-not-connecting-wifi.html",["The four boundaries behind a Wi-Fi printer connection","192.168.50.81/24","association","printer's web page"]],
 ["printer-printing-blank-pages.html",["Three prints, three different systems","printer-generated configuration","same short document from another trusted device"]],
 ["printer-print-queue-stuck-windows-11.html",["A job stuck in the queue is not always a broken spooler","Print Spooler actually stops","two-minute observation"]],
 ["printer-printing-cut-off-pages.html",["A4 versus US Letter: a measurable clipping example","195 + 8 + 8 = 211","17.6 mm","/tools/page-fit"]]
 ];
 for(const [p,parts] of markers){const s=read(p).toLowerCase();for(const part of parts)assert.ok(s.includes(part.toLowerCase()),p+" missing unique educational example: "+part)}
});
test("No approval guarantee is presented in editorial audit",()=>{
 const s=read("ADSENSE-QUALITY-AUDIT.md");
 assert.match(s,/not ready for another AdSense review/i);
 assert.match(s,/No one can guarantee/);
 assert.match(s,/Google-certified CMP/);
});
