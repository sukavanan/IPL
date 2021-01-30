function injectBatsmenFields() {
    let batsmanStr =
    `<div>
        Batsman #@
        <select id="batsman-@-select" name="batsman-@-name" required>
            <option value="" selected disabled> Batsman Name </option>    
        </select>
    </div>`;

    let outputBatsmen = '';
    for(let i = 1; i <= 11; i++) {
        outputBatsmen += batsmanStr.replace(/@/g, i);
    }
    
    document.querySelector('#target-batsmen').innerHTML = outputBatsmen;
}

function injectBowlersFields(numBowlers) {
    let bowlerStr = 
    `<div>
        Bowler #@
        <select id="bowler-@-select" name="bowler-@-name" required>
            <option value="" selected disabled> Bowler Name </option>    
        </select>
        Balls
        <input type="number" name="bowler-@-balls" placeholder="Balls" required>
    </div>`

    let outputBowlers = '';
    for(let i = 1; i <= numBowlers; i++) {
        outputBowlers += bowlerStr.replace(/@/g, i);
    }

    document.querySelector('#target-bowlers').innerHTML = outputBowlers;
}

async function loadBatsmen() {
    await injectBatsmenFields();

    for(let j = 1; j <= 11; j++) {
        let select = document.querySelector(`#batsman-${j}-select`);
       
        for(let i = 0; i < batsmen.length; i++) {
            let option = document.createElement('option');
            option.text = batsmen[i];
            option.value = batsmen[i];
            select.appendChild(option);
        }

        $(`#batsman-${j}-select`).select2();
    }

}

async function loadBowlers() {
    let numBowlers = parseInt(document.querySelector('#bowlers-used').value);
    await injectBowlersFields(numBowlers);

    for(let j = 1; j <= numBowlers; j++) {
        let select = document.querySelector(`#bowler-${j}-select`);
       
        for(let i = 0; i < bowlers.length; i++) {
            let option = document.createElement('option');
            option.text = bowlers[i];
            option.value = bowlers[i];
            select.appendChild(option);
        }

        $(`#bowler-${j}-select`).select2();
    }
}