// usage: node render.js <ep> <outDir> [frames "a-b" | "1,2,3" | all]
const http=require('http'),fs=require('fs'),path=require('path');const {chromium}=require('playwright');
const ROOT=__dirname, ep=process.argv[2], out=process.argv[3], which=process.argv[4]||'all';
fs.mkdirSync(out,{recursive:true});
const types={'.html':'text/html','.js':'text/javascript','.json':'application/json'};
const server=http.createServer((q,r)=>{const p=path.join(ROOT,decodeURIComponent(q.url.split('?')[0]));if(!p.startsWith(ROOT)||!fs.existsSync(p)){r.writeHead(404);return r.end();}r.writeHead(200,{'Content-Type':types[path.extname(p)]||'application/octet-stream'});fs.createReadStream(p).pipe(r);}).listen(0,async()=>{
const b=await chromium.launch();const pg=await b.newPage({viewport:{width:1080,height:1920}});
pg.on('pageerror',e=>console.log('[pageerror]',e.message));pg.on('console',m=>console.log('[page]',m.text()));
await pg.goto(`http://127.0.0.1:${server.address().port}/${process.env.PAGE||'video.html'}?ep=${ep}${process.env.UI?'&ui=1':''}`);await pg.waitForFunction('window.ready===true',null,{timeout:60000});
const info=await pg.evaluate(()=>window.info); fs.writeFileSync(path.join(out,'info.json'),JSON.stringify(info));
const frames= which==='all'?[...Array(info.frames).keys()]: which.includes('-')?(([a,c])=>[...Array(Math.min(c,info.frames)-a).keys()].map(i=>i+a))(which.split('-').map(Number)):which.split(',').map(Number);
const t0=Date.now();
for(const f of frames){const u=await pg.evaluate(i=>window.renderFrame(i),f);fs.writeFileSync(path.join(out,`f${String(f).padStart(5,'0')}.jpg`),Buffer.from(u.split(',')[1],'base64'));}
console.log('done',frames.length,'frames',((Date.now()-t0)/1000).toFixed(1),'s');await b.close();server.close();});
