// Loads the simulation engine straight out of static/index.html and runs the given specs (JSON array on stdin).
const fs=require('fs'),path=require('path');
const html=fs.readFileSync(path.join(__dirname,'..','static','index.html'),'utf8');
const a=html.indexOf('/*SIM-ENGINE-START*/'),b=html.indexOf('/*SIM-ENGINE-END*/');
if(a<0||b<0){console.error('engine markers not found');process.exit(2)}
const Engine=new Function(html.slice(a,b)+'\nreturn SimEngine;')();
let raw='';process.stdin.on('data',d=>raw+=d).on('end',()=>{
  const specs=JSON.parse(raw);
  console.log(JSON.stringify(specs.map(s=>s.complexity?Engine.complexity(s.complexity):Engine.run(s))));
});
