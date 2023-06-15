<meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no">
<title>CGBNvote admin panel</title>
<body id="iz7c">
  <header id="i7wq-2" class="header-banner">
  </header>
  <section id="iq09n-2" class="flex-sect">
    <div id="iq7l-2" class="container-width">
      <div id="ibn2g-2" class="flex-title">CGBNvoteadmin panel
        <br/>
      </div>
      <div id="iy8d-2" class="cards">
        <form method="post" id="itxx7" action="/admin-panel/process" enctype="multipart/form-data" onchange="updateOldForm()">
          <fieldset class="fieldset" id="account">
            <legend class="text">Account</legend>
            <button class="button" type=button onclick=renew_session()>Sessie vernieuwen</button>
            <button class="button" type=button onclick=log_out()>Uitloggen</button>
          </fieldset>
          <fieldset class="fieldset">
            <legend class="text">Kandidatenlijst</legend>
            <p class="text">Vul in het eerste vak de partijnaam in. Vul in het tweede vak een unieke afkorting voor die partij in, die begrijpbaar is voor andere mensen. Dit wordt weergegeven in de uitslagen.</p>
            <div id=candidates></div>
            <button class="button" type=button onclick=add_candidate()>Nieuwe toevoegen</button>
          </fieldset>
          <fieldset class="fieldset" id="dbsettings">
            <legend class="text">Database beheer</legend>
            <button class="button" type=button onclick=reset_auth()>Verwijder alle authenticatiecodes</button>
            <button class="button" type=button onclick=reset_votes()>Verwijder alle stemmen</button>
          </fieldset>
          <fieldset class="fieldset">
            <legend class="text">Andere instellingen</legend>
            <div id="settings"></div>
          </fieldset>
          <div id="i2qefk">
          </div>
          <fieldset id="i1gun">
            <legend id="text">Wijzigingen opslaan</legend>
            <div id="iy8oeq">
              <button type="button" class="button" onclick="save()">Opslaan</button>
              <div id=buffer></div>
              <button type="button" class="button" onclick="reload()">Ongedaan maken</button>
              <input type="hidden" name="username" value={{username}}>
            </div>
          </fieldset>
          <div id="ibo35">
          </div>
        </form>
      </div>
    </div>
  </section>
</body>
<style>* {
  box-sizing: border-box;
  }
  body {
    margin: 0;
  }
  *{
    box-sizing:border-box;
  }
  body{
    margin:0;
  }
  .header-banner{
    padding-top:35px;
    padding-bottom:100px;
    color:#ffffff;
    font-family:Helvetica, serif;
    font-weight:100;
    background-image:url("https://grapesjs.com/img/bg-gr-v.png"), url("https://grapesjs.com/img/work-desk.jpg");
    background-attachment:scroll, scroll;
    background-position:left top, center center;
    background-repeat:repeat-y, no-repeat;
    background-size:contain, cover;
  }
  .container-width{
    width:90%;
    max-width:1150px;
    margin:0 auto;
  }
  .flex-sect{
    background-color:#fafafa;
    padding:50px 0;
    font-family:Helvetica, serif;
  }
  .flex-title{
    margin-bottom:15px;
    font-size:2em;
    text-align:center;
    font-weight:700;
    color:#555;
    padding:5px;
  }
  .cards{
    padding:20px 0;
    display:flex;
    justify-content:space-around;
    flex-flow:wrap;
  }
  #itxx7{
    display:flex;
    flex-direction:column;
    background-repeat:repeat;
    background-position:left top;
    background-attachment:scroll;
    background-size:auto;
    background-image:linear-gradient(to right, #bf387e 0%, #cd5e5e 100%);
    padding:10px 10px 10px 10px;
    box-shadow:0 0 5px 0 black;
    opacity:0.86;
    border-radius:5px 5px 5px 5px;
    width: 50%
  }
  #i7wq-2{
    background-repeat:repeat-y, no-repeat;
    background-position:left top, center center;
    background-attachment:scroll, scroll;
    background-size:contain, cover;
    background-image:url("https://grapesjs.com/img/bg-gr-v.png"), url('https://www.gemeente.nu/content/uploads/sites/5/2017/02/stemmen.jpg');
  }
  .text{
    color:#ffffff;
  }
  #text{
    color:#ffffff;
  }
  .button{
    box-shadow: 0 3px 4px 0 rgba(0,0,0,0.2), 0 6px 20px 0 rgba(0,0,0,0.19);
    border-radius:5px 5px 5px 5px;
    opacity:1;
    border:0px solid white;
    padding:0px 2.5px 0px 2.5px;
    margin: 0 0 5 0;
    height:30px;
    background-repeat:repeat;
    background-position:left top;
    background-attachment:scroll;
    background-size:auto;
    background-image:linear-gradient(#ffffff 0%, #ffffff 100%);
    width:100%;
    display:block;
  }
  .button:hover{
    box-shadow: 0 6px 8px 0 rgba(0,0,0,0.24), 0 17px 50px 0 rgba(0,0,0,0.19);
  }
  #password{
    border-radius:5px 5px 5px 5px;
    opacity:1;
    border:0px solid white;
    padding:0px 2.5px 0px 2.5px;
    height:30px;
    background-repeat:repeat;
    background-position:left top;
    background-attachment:scroll;
    background-size:auto;
    background-image:linear-gradient(#ffffff 0%, #ffffff 100%);
    width:100%;
    display:block;
  }
  .fieldset{
    margin:0 0 6px 0;
  }
  #i1gun{
    margin:0 0 6px 0;
  }
  #iy8oeq{
    height:30px;
    display:flex;
    justify-content: space-between;
  }
  #ifdlg:active{
    box-shadow:0 0 5px 0 black;
  }
  input::-webkit-outer-spin-button, input::-webkit-inner-spin-button{
    -webkit-appearance:none;
    margin:0;
  }
  input[type=number]{
    -moz-appearance:textfield;
  }
  #input{
    display:flex;
    margin:0 0 6px 0;
    width:100%;
    height:30px;
    border-radius:5px 5px 5px 5px;
    border:0px solid white;
    padding: 0 5 0 5;
  }
  #candidateItem{
    border: 1px solid white;
    border-radius:5px 5px 5px 5px;
    margin: 0 0 12px 0;
    padding: 10 ;
  }
  #settingItem {
    display: flex;
    flex-wrap: wrap;
  }
  #buttons{
  justify-content: space-between;
   display:flex
  }
  #buffer{
    margin: 5
  }
  @media only screen and (max-width: 700px) {
  #itxx7{
    width: 90%;
  }
  }
  .switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 34px;
}

p.text{
  margin: 0 0 5 0
}

#dbsettings .button{
  margin: 0 0 6 0
}
</style>
<script type="text/javascript">
 updateOldForm = () => {
        oldForm = document
            .getElementById('itxx7').value;
}

  function update_editor(candidates){

  headerHTML = `<input type="hidden" name="candidate_list" value='${JSON.stringify(candidates)}'>`;
  candidatesHTML = ``;
  footerHTML = ``;

  for (i in candidates){
    candidatesHTML += `
    <div id="candidateItem">
        <input type=text name=display-${i} id="input" placeholder="Weergavenaam" value='${candidates[i][0]}'></input>
        <input type=text name=id-${i} id="input" placeholder="Identificator" value='${candidates[i][1]}'></input>


        <div id=buttons>
            <button class="button" type=button onclick=delete_candidate(${i})>Verwijder</button>
        </div>
    </div>`;
  }
  document.getElementById('candidates').innerHTML = headerHTML + candidatesHTML + footerHTML;
  updateOldForm()
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
    headerHTML = `<input type="hidden" name="setting_list" value='${JSON.stringify(settings)}'>`;
    settingsHTML = ``;
    footerHTML = ``;

    for (i in settings){
        settingsHTML += `
        <div id="settingItem">
        <p id=text name=setting-${i}>${settings[i][0]}</p>
        <input type=text name=setting-value-${i} id="input" placeholder="Weergavenaam" value='${settings[i][1]}'></input>
        </div>`;
    }
    document.getElementById('settings').innerHTML = headerHTML + settingsHTML + footerHTML;
    updateOldForm()
}

function get_settings(){
    i = 0;
    settings = [];
    try{
        while (true){
            settings.push([document.getElementsByName(`setting-${i}`)[0].innerHTML, document.getElementsByName(`setting-value-${i}`)[0].value]);
            i++;
        }
    } catch {return settings};
}

function validateCandidateIds(arr){
  result = []
  for (i in arr) {
    result.push(arr[i][1])
  }
  return new Set(result).size == result.length
}

function save(){
  if (!confirm("Weet u zeker dat u uw wijzigingen wilt opslaan?")){
    return
  }
  candidates = get_candidates()
  update_editor(candidates)
  update_settings(get_settings())

  if (!validateCandidateIds(candidates)){
    alert("Een id mag niet meer dan een keer voorkomen.")
  } else{
    document.getElementById("itxx7").submit();
  }
}
function reload(){
    if (confirm("Weet u zeker dat u uw onopgeslagen wijzigingen ongedaan wilt maken?")){
        location.reload()
    }
}

update_editor({{!candidates}});
update_settings({{!settings}});

</script>
<script>
function reset_auth(){
    fetch('/admin-panel/reset_auth?user={{username}}', {method: 'POST'})
      .then(response => response.text())
      .then(text => alert(text));
};
function reset_votes(){
    fetch('/admin-panel/reset_votes?user={{username}}', {method: 'POST'})
      .then(response => response.text())
      .then(text => alert(text));
};
function log_out(){
    if (confirm("Weet u zeker dat u wilt uitloggen?")){
        location.replace("/admin-panel/log_out")
    }
}
function renew_session(){
    if (oldForm !== ''){
        window.open('/admin-login')
    } else {
        location.href = "/admin-login"
    }
}
</script>
<script>
let oldForm = '';

 window.addEventListener('beforeunload',
    function (e) {

        if (oldForm !== '') {

        e.preventDefault();
    e.returnValue = '';
        }
    });
</script>