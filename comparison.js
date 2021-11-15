date = new Date();
day = String(date.getDate()).padStart(2, '0');
month = String(date.getMonth() + 1).padStart(2, '0');
year = date.getFullYear(); 
f_now = day+'/'+month

function toGet(date, esp_id){
    if(date.length == 9){
        date = '0'+date
    }
    let url = 'https://gaes.pythonanywhere.com/req?date='+date.toString()+'&esp-id='+esp_id.toString();
    //url = 'https://gaes.pythonanywhere.com/req?date=27/10/2021&esp-id=1'
    let request = new XMLHttpRequest()
    request.open('GET', url, false)
    request.send()

    return request.responseText
}

// function format_label_date(iterator){
//     if (month == 5|| month == 7 || month == 10 || month ==12){
//         if (iterator<0){
//             if (Number(day)+iterator==0){
//                 return '30'+'/'+add_left_zero((month-1))
//             }else {
//                 // return add_left_zero(Number(day)+iterator)+'/'+add_left_zero(month)
//                 return add_left_zero(Number(day)+iterator)+'/'+add_left_zero(month)
//             }
//         }else if(iterator>0){
//             if(Number(day)+iterator==32){
//                 if (month == 12){
//                     return '01/01'
//                 }
//                 return '01'+'/'+add_left_zero(month)
//             }else {
//                 return add_left_zero(Number(day)+iterator)+'/'+add_left_zero(month)
//             }
//         }
//     }else if (month == 3){
//         if (iterator<0){
//             if (day+iterator==0){
//                 if ((year % 4 == 0) && ((year % 100 != 0) || (year % 400 == 0))){
//                     return '29'+'/'+add_left_zero((month-1))
//                 }else{
//                     return '28'+'/'+add_left_zero((month-1))
//                 }
//             }else {
//                 return add_left_zero(Number(day)+iterator)+'/'+add_left_zero(month)
//             }
//         }else if(iterator>0){
//             if(Number(day)+iterator==32){
//                 return '01'+'/'+add_left_zero(month+1)
//             }else {
//                 return add_left_zero(Number(day)+iterator)+'/'+add_left_zero(month)
//             }
//         }
//     }else if(month == 1 || month == 8){
//         if (iterator<0){
//             if (Number(day)+iterator==0){
//                 return '31'+'/'+add_left_zero((month-1))
//             }else {
//                 return add_left_zero(Number(day)+iterator)+'/'+add_left_zero(month)
//             }
//         }else if(iterator>0){
//             if(Number(day)+iterator==32){
//                 return '01'+'/'+add_left_zero(month+1)
//             }else {
//                 return add_left_zero(Number(day)+iterator)+'/'+add_left_zero(month)
//             }
//         }
//     }else{
//         if (iterator<0){
//             if (Number(day)+iterator==0){
//                 return '31'+'/'+add_left_zero((month-1))
//             }else {                
//                 return add_left_zero(Number(day)+iterator)+'/'+add_left_zero(month)
//             }
//         }else if(iterator>0){
//             if(Number(day)+iterator==31){
//                 return '01'+'/'+add_left_zero(month+1)
//             }else {                
//                 return add_left_zero(Number(day)+iterator)+'/'+add_left_zero(month)
//             }
//         }
//     }
// }

function format_label_date(iterator){
    if (month == 5|| month == 7 || month == 10 || month ==12){
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
    }else if (month == 3){
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
        
    }else if(month == 1 || month == 8){
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
    }else{
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
    }
}

function comparison(esp_id){
    try{
        data = toGet(f_now+'/'+year, esp_id)
        // data = toGet('17/09'+'/'+year, esp_id)
        today = JSON.parse(data)
        average_spent = 0
        count = 0
        for(i = -3; i<=-1; i++){
            olddata = toGet(format_label_date(i)+'/'+year, esp_id)
            olddata = JSON.parse(olddata)
            console.log('olddata: ', olddata.data.spent)
            average_spent += olddata.data.spent
            console.log('spent', average_spent)
            count++ 
        }

        average_spent /= count
        console.log('average: ', average_spent)

        // old_data = toGet(format_label_date(-1)+'/'+year, esp_id)
        // yesterday = JSON.parse(old_data)
        // console.log('yesterday: ', yesterday)
        
        estimated_gain = today.data.prediction * (today.data.eficience/100)
        console.log('estimated gain = ', estimated_gain)

        //console.log('old spent = ', yesterday.data.spent)

        console.log('estimated gain 120%', estimated_gain * 1.2)
        console.log('estimated gain 110%', estimated_gain * 1.1)
        console.log('estimated gain 100%', estimated_gain)
        console.log('estimated gain 90%', estimated_gain * 0.9)
        
        if (average_spent >= estimated_gain * 1.2){
            console.log('data.spent >= 120% estimated_gain')
            document.write('Economia extremamente recomendada')
        }else if(average_spent >= estimated_gain * 1.1){
            console.log('data.spent >= 110% estimated_gain')
            document.write('Economia fortemente recomendada')
        }else if(average_spent >= estimated_gain){
            console.log('data.spent >= estimated_gain')
            document.write('Economia recomendada')
        }else if(average_spent >= estimated_gain * 0.9){
            console.log('data.spent >= 90% estimated_gain')
            document.write('Nível de energia aceitável')
        }else{
            console.log('data.spent >= 80% estimated_gain')
            document.write('Nível de energia boa')
        }
    }catch{
        document.write('Not enough data yet')
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

function main(){
    comparison(1)
}

main()

