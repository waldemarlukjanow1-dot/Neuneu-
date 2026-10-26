const http=require('http'),fs=require('fs'),path=require('path');const {chromium}=require('playwright');
const ROOT=path.join(__dirname,'..'), page=process.argv[2], out=process.argv[3];
const server=http.createServer((q,r)=>{const p=path.join(ROOT,q.url.split('?')[0]);if(!fs.existsSync(p)){r.writeHead(404);return r.end();}r.writeHead(200,{'Content-Type':p.endsWith('.html')?'text/html':'text/javascript'});fs.createReadStream(p).pipe(r);}).listen(0,async()=>{
const b=await chromium.launch();const pg=await b.newPage({viewport:{width:2400,height:1500}});pg.on('pageerror',e=>console.log('ERR',e.message));pg.on('console',m=>console.log(m.text()));
await pg.goto(`http://127.0.0.1:${server.address().port}/stick/${page}`);await pg.waitForFunction('window.done',null,{timeout:60000});
await (await pg.$('canvas')).screenshot({path:out});await b.close();server.close();});
