const BASE=import.meta.env.VITE_API_BASE || '';
export type Dataset={id:string;name:string;rows:number;columns:number};
export async function request<T>(path:string,key:string,init:RequestInit={}):Promise<T>{
 const headers:Record<string,string>={'X-API-Key':key};
 if(init.body && !(init.body instanceof FormData))headers['Content-Type']='application/json';
 const res=await fetch(BASE+path,{...init,headers:{...headers,...init.headers}});
 if(!res.ok)throw new Error(`${res.status}: ${await res.text()}`);
 return res.json() as Promise<T>;
}
