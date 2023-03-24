function update_editor(candidates){

  headerHTML = ``;
  candidatesHTML = ``;
  footerHTML = ``;

  for (i in candidates){
    candidatesHTML += `
    <div id="candidateItem">
        <input type=text name=display-${i} id="input" placeholder="Weergavenaam" value= ${candidates[i][0]}></input>
        <input type=text name=id-${i} id="input" placeholder="Identificator" value= ${candidates[i][1]}></input>


        <div id=buttons>
            <button id=button type=button onclick=delete_candidate(${i})>Verwijder</button>
            <!--
            <div id=buffer></div>
            <button id=button type=button onclick=add_candidate()>Nieuwe toevoegen</button> -->
        </div>
    </div>`;
  }
  document.getElementById('candidates').innerHTML = headerHTML + candidatesHTML + footerHTML;
}

function get_candidates(){
    let i = 0;
    candidates = [];
    try{
        while (true){
            candidates.push([document.getElementsByName(`display-${i}`)[0].value, document.getElementsByName(`id-${i}`)[0].value]);
            i++;
        }
    } catch {return candidates};
}

function delete_candidate(candidate){
    candidates = get_candidates();
    candidates.splice(candidate, 1);
    update_editor(candidates);
}

function add_candidate(){
    candidates = get_candidates();
    candidates.push(["", ""]);
    update_editor(candidates);
}

function update_settings(settings){
    headerHTML = ``;
    settingsHTML = ``;
    footerHTML = ``;

    for (i in settings){
        settingsHTML += `
        <div id="settingItem">
        <p id=text>${settings[i][0]}</p>
        <input type=text name=test-${i} id="input" placeholder="Weergavenaam" value= ${settings[i][1]}></input>
        </div>`;
    }
    document.getElementById('settings').innerHTML = headerHTML + settingsHTML + footerHTML;
}
update_editor({candidates});
update_settings({settings});