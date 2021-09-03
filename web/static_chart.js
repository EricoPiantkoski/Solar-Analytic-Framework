async function get_api_data(date, esp_id, flag = null) {
    if(date.length == 9){
        date = "0"+date
    }
    //console.log(date.length)
    let url = 'https://gaes.pythonanywhere.com/req?date='+date.toString()+'&esp-id='+esp_id.toString();
    let obj = null;
    
    try {
        obj = await (await fetch(url)).json();
    } catch(e) {
        console.log('error');
    }
        if (flag){
            if(flag == 0){ // flag == 0 -> obj
                return obj
            }else if(flag == 1){ // flag == 1 -> id
                return obj.id_esp
            }else if(flag == 2){ // flag == 2 -> date_log
                return obj.date_log
            }else if(flag == 3){ // flag == 3 -> spent
                return obj.data.spent
            }else if(flag == 4){ // flag == 4 -> gain
                return obj.data.gain
            }else if(flag == 5){ // flag == 5 -> prediction
                console.log(obj)
                return obj.data.prediction
            }
        }
        return obj
    }

async function set_chart(esp_id='1', date){

    esp_data = await get_api_data(date, esp_id);
    var ctx = document.getElementsByClassName("bar-chart");
    //solve_data()          
    var charGraph = new Chart(ctx, {
        type: 'bar',
        data: {
            // Legendas das Barras
            labels: [
                format_label_date(-2)+'/'+month, 
                format_label_date(-1)+'/'+month, 
                f_now+'/'+year, 
                format_label_date(1)+'/'+month, 
                format_label_date(2)+'/'+month, 
                format_label_date(3)+'/'+month,
                format_label_date(4)+'/'+month
            ],
            datasets: [{
                label: 'Aquisição',
                data: [
                    await get_api_data(format_label_date(-2)+'/'+month+'/'+year, esp_id, 4), 
                    await get_api_data(format_label_date(-1)+'/'+month+'/'+year, esp_id, 4),
                    await get_api_data(f_now+'/'+year, esp_id, 4), 
                    await get_api_data(format_label_date(1)+'/'+month+'/'+year, esp_id, 4), 
                    await get_api_data(format_label_date(2)+'/'+month+'/'+year, esp_id, 4), 
                    await get_api_data(format_label_date(3)+'/'+month+'/'+year, esp_id, 4), 
                    await get_api_data(format_label_date(4)+'/'+month+'/'+year, esp_id, 4),
                ],
                backgroundColor: [
                    'rgba(84, 151, 90, 0.5)'
                ],
                borderColor: [
                    'rgba(84, 151, 90, 1)',
                                            
                ],
                // Define a espessura da borda dos retângulos
                borderWidth: 1
            },
            {
                label: 'Gasto',
                data: [
                    await get_api_data(format_label_date(-2)+'/'+month+'/'+year, esp_id, 3), 
                    await get_api_data(format_label_date(-1)+'/'+month+'/'+year, esp_id, 3),
                    await get_api_data(f_now+'/'+year, esp_id, 3), 
                    await get_api_data(format_label_date(1)+'/'+month+'/'+year, esp_id, 3), 
                    await get_api_data(format_label_date(2)+'/'+month+'/'+year, esp_id, 3), 
                    await get_api_data(format_label_date(3)+'/'+month+'/'+year, esp_id, 3), 
                    await get_api_data(format_label_date(4)+'/'+month+'/'+year, esp_id, 3),
                ],
                backgroundColor: [                           
                    'rgba(255, 99, 132, 0.5)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)'                       
                ],
                // Define a espessura da borda dos retângulos
                borderWidth: 1
            },
        {
            label: 'Previsão',
                data: [
                    await get_api_data(format_label_date(-2)+'/'+month+'/'+year, esp_id, 5), 
                    await get_api_data(format_label_date(-1)+'/'+month+'/'+year, esp_id, 5),
                    await get_api_data(f_now+'/'+year, esp_id, 5), 
                    await get_api_data(format_label_date(1)+'/'+month+'/'+year, esp_id, 5), 
                    await get_api_data(format_label_date(2)+'/'+month+'/'+year, esp_id, 5), 
                    await get_api_data(format_label_date(3)+'/'+month+'/'+year, esp_id, 5), 
                    await get_api_data(format_label_date(4)+'/'+month+'/'+year, esp_id, 5),
                ],
                backgroundColor: [
                    'rgba(255, 206, 86, 0.5)'
                ],
                borderColor: [
                    'rgba(255, 206, 86, 1)'                            
                ],
                // Define a espessura da borda dos retângulos
                borderWidth: 1
        }]
        },
        options: {
            legend:{
                display: false,
                position: 'left'
            },
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}

function format_label_date(iterator){
    if (month == 5|| month == 7 || month == 10 || month ==12){
        if (iterator<0){
            if (Number(day)-iterator==-1){
                return '29'
            }else if (Number(day)-iterator==0){
                return '30'
            }else {
                return Number(day)+iterator
            }
        }else if(iterator>0){
            if(Number(day)+iterator==35){
                return '04'
            }else if(Number(day)+iterator==34){
                return '03'
            }else if(Number(day)+iterator==33){
                return '02'
            }else if(Number(day)+iterator==32){
                return '01'
            }else {
                return Number(day)+iterator
            }
        }
    }else if (month == 3){
        if (iterator<0){
            if (day-iterator==-1){
                if ((year % 4 == 0) && ((year % 100 != 0) || (year % 400 == 0))){
                    return '28'
                }else{
                    return '27'
                }
            }else if (day-iterator==0){
                if ((year % 4 == 0) && ((year % 100 != 0) || (year % 400 == 0))){
                    return '29'
                }else{
                    return '28'
                }
            }else {
                return Number(day)+iterator
            }
        }else if(iterator>0){
            if(Number(day)+iterator==35){
                return '04'
            }else if(Number(day)+iterator==34){
                return '03'
            }else if(Number(day)+iterator==33){
                return '02'
            }else if(Number(day)+iterator==32){
                return '01'
            }else {
                return Number(day)+iterator
            }
        }
    }else if(month == 1 || month == 8){
        
        if (iterator<0){
            if (Number(day)-iterator==-1){
                return '30'
            }else if (Number(day)-iterator==0){
                return '31'
            }else {
                return Number(day)+iterator
            }
        }else if(iterator>0){
            if(Number(day)+iterator==35){
                return '04'
            }else if(Number(day)+iterator==34){
                return '03'
            }else if(Number(day)+iterator==33){
                return '02'
            }else if(Number(day)+iterator==32){
                return '01'
            }else {
                return Number(day)+iterator
            }
        }
    }else{
        if (iterator<0){
            if (Number(day)-iterator==-1){
                return '30'
            }else if (Number(day)-iterator==0){
                return '31'
            }else {                
                return Number(day)+iterator
            }
        }else if(iterator>0){
            if(Number(day)+iterator==34){
                return '04'
            }else if(Number(day)+iterator==33){
                return '03'
            }else if(Number(day)+iterator==32){
                return '02'
            }else if(Number(day)+iterator==31){
                return '01'
            }else {                
                return Number(day)+iterator
            }
        }
    }
}

date = new Date();
day = String(date.getDate()).padStart(2, '0');
month = String(date.getMonth() + 1).padStart(2, '0');
year = date.getFullYear(); 
f_now = day+'/'+month
//console.log(f_now)

set_chart(1, f_now+'/'+year);