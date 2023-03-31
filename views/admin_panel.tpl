<meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no">
<title>CGBNvote admin panel</title>
<body id="iz7c">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no"/>
  <header id="i7wq-2" class="header-banner">
  </header>
  <section id="iq09n-2" class="flex-sect">
    <div id="iq7l-2" class="container-width">
      <div id="ibn2g-2" class="flex-title">CGBNvoteadmin panel
        <br/>
      </div>
      <div id="iy8d-2" class="cards">
        <form method="post" id="itxx7" action="/vote-admin/process" enctype="multipart/form-data">
          <fieldset id="fieldset">
            <legend id="i9w0u">Kandidatenlijst</legend>
            <div id=candidates></div>
            <button id=button type=button onclick=add_candidate()>Nieuwe toevoegen</button>
          </fieldset>
          <fieldset id="ispc8">
            <legend id="i0b1u">Andere instellingen</legend>
            <div id="settings"></div>
          </fieldset>
          <div id="i2qefk">
          </div>
          <fieldset id="i1gun">
            <legend id="text">Wijzigingen opslaan</legend>
            <div id="iy8oeq">
              <button type="button" id="button" onclick="save()">Opslaan</button>
              <div id=buffer></div>
              <input type="hidden" name="username" value={{username}}>
              <input type="password" name="password" required id="password" placeholder="wachtwoord"/>
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
  #ispc8{
    margin:0 0 6px 0;
  }
  #i9w0u{
    color:#ffffff;
  }
  #i0b1u{
    color:#ffffff;
  }
  #text{
    color:#ffffff;
  }
  #button{
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
  #fieldset{
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

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #ccc;
  -webkit-transition: .4s;
  transition: .4s;
}

.slider:before {
  position: absolute;
  content: "";
  height: 26px;
  width: 26px;
  left: 4px;
  bottom: 4px;
  background-color: white;
  -webkit-transition: .4s;
  transition: .4s;
}

input:checked + .slider {
  background-color: #2196F3;
}

input:focus + .slider {
  box-shadow: 0 0 1px #2196F3;
}

input:checked + .slider:before {
  -webkit-transform: translateX(26px);
  -ms-transform: translateX(26px);
  transform: translateX(26px);
}

/* Rounded sliders */
.slider.round {
  border-radius: 34px;
}

.slider.round:before {
  border-radius: 50%;
}
</style>
<script type="text/javascript">
  function update_editor(candidates){

  headerHTML = `<input type="hidden" name="candidate_list" value='${JSON.stringify(candidates)}'>`;
  candidatesHTML = ``;
  footerHTML = ``;

  for (i in candidates){
  console.log(candidates[i][0])
    candidatesHTML += `
    <div id="candidateItem">
        <input type=text name=display-${i} id="input" placeholder="Weergavenaam" value='${candidates[i][0]}'></input>
        <input type=text name=id-${i} id="input" placeholder="Identificator" value= '${candidates[i][1]}'></input>


        <div id=buttons>
            <button id=button type=button onclick=delete_candidate(${i})>Verwijder</button>
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
    headerHTML = `<input type="hidden" name="setting_list" value=${JSON.stringify(settings)}>`;
    settingsHTML = ``;
    footerHTML = ``;

    for (i in settings){
        settingsHTML += `
        <div id="settingItem">
        <p id=text name=setting-${i}>${settings[i][0]}</p>
        <input type=text name=setting-value-${i} id="input" placeholder="Weergavenaam" value= ${settings[i][1]}></input>
        </div>`;
    }
    document.getElementById('settings').innerHTML = headerHTML + settingsHTML + footerHTML;
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

function save(){
  update_editor(get_candidates())
  update_settings(get_settings())

  if (document.getElementById("password").value == ""){
    alert("Vul het wachtwoord-veld in.")
  } else{


    document.getElementById("itxx7").submit();
   }
}
update_editor({{!candidates}});
update_settings({{!settings}});
</script>