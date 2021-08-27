async function get_api_data(esp_id, date, flag = null) {
    let url = 'http://127.0.0.1:5000/req?esp-id='+esp_id.toString()+'&date='+date.toString();
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
        if (flag){
            if(flag == 0){ // flag == 0 -> obj
                return obj
            }else if(flag == 'id'){ // flag == 1 -> id
                return obj.id
            }else if(flag == 'date_log'){ // flag == 2 -> date_log
                return obj.date_log
            }else if(flag == 'spent'){ // flag == 3 -> spent
                return obj.data.spent
            }else if(flag = 'gain'){ // flag == 4 -> gain
                return obj.data.gain
            }else if(flag = 'prediction'){ // flag == 5 -> prediction
                return obj.data.prediction
            }
        }
        return obj
    }

async function set_chart(esp_id='1', date){

    esp_data = await get_api_data(esp_id, date);
    var ctx = document.getElementsByClassName("bar-chart");
    //solve_data()          
    var charGraph = new Chart(ctx, {
        type: 'bar',
        data: {
            // Legendas das Barras
            labels: [
                format_label_date(-2)+'/'+month, 
                format_label_date(-1)+'/'+month, 
                f_now, 
                format_label_date(1)+'/'+month, 
                format_label_date(2)+'/'+month, 
                format_label_date(3)+'/'+month,
                format_label_date(4)+'/'+month
            ],
            datasets: [{
                label: 'Aquisição',
                data: [
                    esp_data.data.gain, 
                    9, 
                    await get_api_data(esp_id, f_now, 4), 
                    19, 
                    21, 
                    7, 
                    8
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
                data: [10, 9, 12, 19, 21, 7, 8],
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
                data: [10, 9, 12, 19, 21, 7, 8],
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
            if (day-iterator==-1){
                return '29'
            }else if (day-iterator==0){
                return '30'
            }else {
                return Number(day)+iterator
            }
        }else if(iterator>0){
            if(day+iterator==35){
                return '04'
            }else if(day+iterator==34){
                return '03'
            }else if(day+iterator==33){
                return '02'
            }else if(day+iterator==32){
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
            if(day+iterator==35){
                return '04'
            }else if(day+iterator==34){
                return '03'
            }else if(day+iterator==33){
                return '02'
            }else if(day+iterator==32){
                return '01'
            }else {
                return Number(day)+iterator
            }
        }
    }else if(month == 1 || month == 8){
        
        if (iterator<0){
            if (day-iterator==-1){
                return '30'
            }else if (day-iterator==0){
                return '31'
            }else {
                return Number(day)+iterator
            }
        }else if(iterator>0){
            if(day+iterator==35){
                return '04'
            }else if(day+iterator==34){
                return '03'
            }else if(day+iterator==33){
                return '02'
            }else if(day+iterator==32){
                return '01'
            }else {
                return Number(day)+iterator
            }
        }
    }else{
        if (iterator<0){
            if (day-iterator==-1){
                return '30'
            }else if (day-iterator==0){
                return '31'
            }else {
                return Number(day)+iterator
            }
        }else if(iterator>0){
            if(day+iterator==34){
                return '04'
            }else if(day+iterator==33){
                return '03'
            }else if(day+iterator==32){
                return '02'
            }else if(day+iterator==31){
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

set_chart(1, f_now);