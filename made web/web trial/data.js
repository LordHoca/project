const name = "Fauzan Fadhilah"
let age = 16
let biodata = document.getElementById('biodata');
function generateBiodata(){
console.log(`Nama Saya Adalah ${name} dan Usia Saya Adalah ${age}`)
}

function generasi(age){
 let generasi;

 if (age < 18){
    generasi = "Golongan Anak - Anak"
 }
 else if (age >= 18 && age <= 20) {
    generasi = "Golongan Remaja"
 }
 else{
    generasi = "Golongan Dewasa"
 }

return generasi

}

console.log("Nama Saya : "+ name)
console.log("Usia Saya : "+ age)
generateBiodata()
console.log("Golongan Saya : ", generasi(age))
biodata.innerHTML = `Nama Saya : ${name} <br> Usia Saya : ${age} <br> ${generasi(age)}`;

function toggleMenu(){
   const menu = docuument.getElementById()
}