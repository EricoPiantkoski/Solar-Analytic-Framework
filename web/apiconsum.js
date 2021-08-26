async function load() {
    let url = 'http://127.0.0.1:5000/req?esp-id=1&date=04/12';
    let obj = null;
    
    try {
        obj = await (await fetch(url)).json();
    } catch(e) {
        console.log('error');
    }
    
    // console.log(obj);
    // console.log(obj.id);
    // console.log(obj.date_log.substring(0,5));
    // console.log(obj.data.spent);
    // console.log(obj.data.gain);
    var datajson = JSON.stringify(obj) 
    //console.log(r);
    //console.log(typeof(r))
    return obj
}

async function recoverData(promisseData){
    resp = await load()
    console.log(resp)
    const id = resp.id
    console.log(id)
    return resp
}
response = recoverData()
console.log(id)
// let r = load();
//var data = JSON.stringify(response) 
// console.log(r);
//console.log(load());

//let datat = null;

// window.onload = function() {

// };