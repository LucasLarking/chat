
//   ###########  TAG COLORS ###########
let colors = [
    '#FFF5E4',
    '#FFE3E1',
    '#FFD1D1',
    '#FF9494',
    '#B1B2FF',
    '#AAC4FF',
    '#D2DAFF',
    '#CDF0EA',
    '#ECC5FB',
    '#FAF4B7',
    '#ECC5FB',
    '#A7D2CB',
    '#F2D388',
    '#F675A8',
    '#FFCCB3',
    '#F29393',
    '#FFB3B3',
    '#FFE9AE',
    '#C1EFFF',
    '#B2C8DF',
    '#C4DFAA',
    '#F2D7D9',
    '#D3CEDF',
    '#CDF0EA',
    '#9ADCFF',
    '#B4CFB0',
    '#C3DBD9',
    '#FDCEB9',
    '#FFEFEF',
    '#EEC373',
    '#96C7C1',
    '#FFDEFA',
    '#C6D57E',






]

let subjects = document.querySelectorAll('.subject');
for (let index = 0; index < subjects.length; index++) {

    const random = Math.floor(Math.random() * colors.length);
    console.log(random)
    subjects[index].style.backgroundColor = colors[random];
}

//  ###########  TAG COLORS ###########