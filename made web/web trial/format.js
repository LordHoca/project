pemasukan = prompt("Masukan saldo anda hari ini Rp.  ");
pengeluaran = prompt("Masukan saldo pengeluaran anda hari ini Rp.  ");
let saldoAkhir = pemasukan - pengeluaran;
alert("Saldo anda hari ini tersisa: " + saldoAkhir); 

const day = ["Ahad", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"];
const bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"];
const date = new Date();
const month = date.getMonth() + 1;
nameofmonth = bulan[date.getMonth()];
nameofday= day[date.getDay()]
alert(`Pada hari ${nameofday} bulan ${nameofmonth}, saldo akhir anda adalah Rp. ${saldoAkhir}`);
