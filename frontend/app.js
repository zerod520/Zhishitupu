const titles = {'knowledge-graph':'知识图谱','data-governance':'数据治理','model-governance':'模型治理'};
const descriptions = {'knowledge-graph':'资产、损伤与失效之间的关系查询入口。','data-governance':'数据接入、标准化与质量管理边界。','model-governance':'模型登记、版本审批与外部预测服务管理边界。'};
let requestVersion = 0;
const make = (tag, text) => {const el=document.createElement(tag);el.textContent=text;return el;};
async function load(module) {
  const version=++requestVersion;
  document.querySelectorAll('[data-module]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.module===module)));
  document.querySelector('#title').textContent=titles[module];
  document.querySelector('#description').textContent=descriptions[module];
  const status=document.querySelector('#status'), content=document.querySelector('#content');
  status.className='';status.textContent='正在加载…';content.replaceChildren();
  try {
    const response=await fetch(`/api/v1/${module}/${module==='knowledge-graph'?'snapshot':'status'}`,{signal:AbortSignal.timeout(15000)});
    if(!response.ok) {const error=await response.json();throw new Error(error.detail||`请求失败 (${response.status})`);}
    const data=await response.json();if(version!==requestVersion)return;
    if(module==='knowledge-graph') {
      status.textContent=data.mode==='demo'?'演示模式 · 合成数据 · 只读 · 未连接真实数据库':'Neo4j 模式 · 只读实时查询';
      const table=document.createElement('table'), head=document.createElement('tr');
      ['节点名称','类型','标识'].forEach(t=>head.append(make('th',t)));table.append(head);
      data.nodes.forEach(n=>{const row=document.createElement('tr');[n.name,n.labels.join(', '),n.id].forEach(t=>row.append(make('td',t)));table.append(row);});
      content.append(table,make('h2','关系'));
      data.edges.forEach(e=>content.append(make('p',`${e.source} → ${e.type} → ${e.target}`)));
      if(!data.nodes.length)content.append(make('p','当前数据库没有节点。'));
    } else {
      status.textContent='基础占位 · 以下能力尚未实现';
      const list=document.createElement('ul');data.capabilities.forEach(c=>list.append(make('li',c)));content.append(list);
    }
  } catch(error) {if(version!==requestVersion)return;status.className='error';status.textContent=error.message;content.append(make('p','请检查后端服务或数据库连接，然后点击模块重试。'));}
}
document.querySelectorAll('[data-module]').forEach(b=>b.addEventListener('click',()=>load(b.dataset.module)));
load('knowledge-graph');
