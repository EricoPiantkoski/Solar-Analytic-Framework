async function api_consum(date, esp_id, flag = null) {
    //console.log(date)
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
        return 0
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
                return obj.data.prediction
            }else if(flag == 6){ // flag == 6 -> eficience
                return obj.data.eficience
            }
        }
        return obj
    }

async function set_chart(esp_id='1', date){
    console.log('Eficience: ', await api_consum(format_label_date(-4)+'/'+year,esp_id,6), '%')
    var eficience = await api_consum(f_now+'/'+year, esp_id, 6)

    esp_data = await api_consum(date, esp_id);
    var ctx = document.getElementsByClassName("bar-chart");
    //solve_data()          
    var charGraph = new Chart(ctx, {
        type: 'bar',
        data: {
            // Legendas das Barras
            labels: [
                add_left_zero(format_label_date(-4)), 
                add_left_zero(format_label_date(-3)), 
                add_left_zero(format_label_date(-2)),
                add_left_zero(format_label_date(-1)), 
                f_now, 
                add_left_zero(format_label_date(1)),
                add_left_zero(format_label_date(2))
            ],
            datasets: [{
                label: 'Aquisição',
                data: [
                    await api_consum(format_label_date(-4)+'/'+year, esp_id, 4), 
                    await api_consum(format_label_date(-3)+'/'+year, esp_id, 4),
                    await api_consum(format_label_date(-2)+'/'+year, esp_id, 4),
                    await api_consum(format_label_date(-1)+'/'+year, esp_id, 4), 
                    await api_consum(f_now+'/'+year, esp_id, 4),
                    await api_consum(format_label_date(1)+'/'+year, esp_id, 4), 
                    await api_consum(format_label_date(2)+'/'+year, esp_id, 4),
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
                    await api_consum(format_label_date(-4)+'/'+year, esp_id, 3), 
                    await api_consum(format_label_date(-3)+'/'+year, esp_id, 3),
                    await api_consum(format_label_date(-2)+'/'+year, esp_id, 3),
                    await api_consum(format_label_date(-1)+'/'+year, esp_id, 3), 
                    await api_consum(f_now+'/'+year, esp_id, 3),
                    await api_consum(format_label_date(1)+'/'+year, esp_id, 3), 
                    await api_consum(format_label_date(2)+'/'+year, esp_id, 3),
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
                    // await api_consum(format_label_date(-4)+'/'+year, esp_id, 5)*0.1, 
                    // await api_consum(format_label_date(-3)+'/'+year, esp_id, 5)*0.1,
                    // await api_consum(format_label_date(-2)+'/'+year, esp_id, 5)*0.1,
                    // await api_consum(format_label_date(-1)+'/'+year, esp_id, 5)*0.1, 
                    // await api_consum(f_now+'/'+year, esp_id, 5)*0.1,
                    // await api_consum(format_label_date(1)+'/'+year, esp_id, 5)*0.1, 
                    // await api_consum(format_label_date(2)+'/'+year, esp_id, 5)*0.1,

                    await api_consum(format_label_date(-4)+'/'+year, esp_id, 5)* eficience/100, 
                    await api_consum(format_label_date(-3)+'/'+year, esp_id, 5)* eficience/100,
                    await api_consum(format_label_date(-2)+'/'+year, esp_id, 5)* eficience/100,
                    await api_consum(format_label_date(-1)+'/'+year, esp_id, 5)* eficience/100, 
                    await api_consum(f_now+'/'+year, esp_id, 5)* eficience/100,
                    await api_consum(format_label_date(1)+'/'+year, esp_id, 5)* eficience/100, 
                    await api_consum(format_label_date(2)+'/'+year, esp_id, 5)* eficience/100,
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
    //document.write('aaa')
}

function format_label_date(iterator){
    if (month == 5|| month == 7 || month == 10 || month ==12){
        if (iterator<0){
            if (Number(day)+iterator==-3){
                return '27'+'/'+add_left_zero((month-1))
            }else if (Number(day)+iterator==-2){
                return '28'+'/'+add_left_zero((month-1))
            }else if (Number(day)+iterator==-1){
                return '29'+'/'+add_left_zero((month-1))
            }else if (Number(day)+iterator==0){
                return '30'+'/'+add_left_zero((month-1))
            }else {
                // return add_left_zero(Number(day)+iterator)+'/'+add_left_zero(month)
                return add_left_zero(Number(day)+iterator)+'/'+add_left_zero(month)
            }
        }else if(iterator>0){
            if(Number(day)+iterator==33){
                if (month == 12){
                    return '02/01'
                }
                return '02'+'/'+add_left_zero(month)
            }else if(Number(day)+iterator==32){
                if (month == 12){
                    return '01/01'
                }
                return '01'+'/'+add_left_zero(month)
            }else {
                return add_left_zero(Number(day)+iterator)+'/'+add_left_zero(month)
            }
        }
    }else if (month == 3){
        if (iterator<0){
            if (day+iterator==-3){
                if ((year % 4 == 0) && ((year % 100 != 0) || (year % 400 == 0))){
                    return '26'+'/'+add_left_zero((month-1))
                }else{
                    return '25'+'/'+add_left_zero((month-1))
                }
            }else if (day+iterator==-2){
                if ((year % 4 == 0) && ((year % 100 != 0) || (year % 400 == 0))){
                    return '27'+'/'+add_left_zero((month-1))
                }else{
                    return '26'+'/'+add_left_zero((month-1))
                }
            }else if (day+iterator==-1){
                if ((year % 4 == 0) && ((year % 100 != 0) || (year % 400 == 0))){
                    return '28'+'/'+add_left_zero((month-1))
                }else{
                    return '27'+'/'+add_left_zero((month-1))
                }
            }else if (day+iterator==0){
                if ((year % 4 == 0) && ((year % 100 != 0) || (year % 400 == 0))){
                    return '29'+'/'+add_left_zero((month-1))
                }else{
                    return '28'+'/'+add_left_zero((month-1))
                }
            }else {
                return add_left_zero(Number(day)+iterator)+'/'+add_left_zero(month)
            }
        }else if(iterator>0){
            if(Number(day)+iterator==33){
                return '02'+'/'+add_left_zero(month+1)
            }else if(Number(day)+iterator==32){
                return '01'+'/'+add_left_zero(month+1)
            }else {
                return add_left_zero(Number(day)+iterator)+'/'+add_left_zero(month)
            }
        }
    }else if(month == 1 || month == 8){
        if (iterator<0){
            if (Number(day)+iterator==-3){
                return '28'+'/'+add_left_zero((month-1))
            }else if (Number(day)+iterator==-2){
                return '29'+'/'+add_left_zero((month-1))
            }else if (Number(day)+iterator==-1){
                return '30'+'/'+add_left_zero((month-1))
            }else if (Number(day)+iterator==0){
                return '31'+'/'+add_left_zero((month-1))
            }else {
                return add_left_zero(Number(day)+iterator)+'/'+add_left_zero(month)
            }
        }else if(iterator>0){
            if(Number(day)+iterator==33){
                return '02'+'/'+add_left_zero(month+1)
            }else if(Number(day)+iterator==32){
                return '01'+'/'+add_left_zero(month+1)
            }else {
                return add_left_zero(Number(day)+iterator)+'/'+add_left_zero(month)
            }
        }
    }else{
        if (iterator<0){
            if (Number(day)+iterator==-3){
                return '28'+'/'+add_left_zero((month-1))
            }else if (Number(day)+iterator==-2){
                return '29'+'/'+add_left_zero((month-1))
            }else if (Number(day)+iterator==-1){
                return '30'+'/'+add_left_zero((month-1))
            }else if (Number(day)+iterator==0){
                return '31'+'/'+add_left_zero((month-1))
            }else {                
                return add_left_zero(Number(day)+iterator)+'/'+add_left_zero(month)
            }
        }else if(iterator>0){
            if(Number(day)+iterator==32){
                return '02'+'/'+add_left_zero(month+1)
            }else if(Number(day)+iterator==31){
                return '01'+'/'+add_left_zero(month+1)
            }else {                
                return add_left_zero(Number(day)+iterator)+'/'+add_left_zero(month)
            }
        }
    }
}

function add_left_zero(item){
    item = item.toString()
    if(item.length == 1){
        return "0"+item
    }else{
        return(item)
    }
}   

date = new Date();
day = String(date.getDate()).padStart(2, '0');
month = String(date.getMonth() + 1).padStart(2, '0');
year = date.getFullYear(); 
f_now = day+'/'+month
//console.log(f_now)

set_chart(1, f_now+'/'+year);

// d = new Date()
// nd = new Date()
// nd.setDate(d.getDate()-14);
// document.write(nd);
// m = String(nd.getMonth()+1)
// document.write(String(nd.getMonth()+1).padStart(2, '0'))