<meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no">
<title>CGBNvote</title>
<body id="iz7c">
  <header id="i7wq-2" class="header-banner">
  </header>
  <section id="iq09n-2" class="flex-sect">
    <div id="iq7l-2" class="container-width">
      <div id="ibn2g-2" class="flex-title">CGBNvote
      </div>
      <div id="iprpw-2" class="flex-desc">Stem hier voor de online CGBN verkiezingen.
        <br/>
      </div>
      <div id="iy8d-2" class="cards">
        <form method="post" id="itxx7" action="/vote">
          <fieldset id="ih2z2">
            <legend id="i9w0u">Voer je leerlingnummer in (voor authenticatie):</legend>
            <input type="number" id="user" name="user" required/>
          </fieldset>
          <fieldset id="ispc8">
            <legend id="i0b1u">Voer je authenticatiecode in:</legend>
            <button type="button" id="Button_sendCode">Stuur code</button>
            <input type="password" id="imzij" name="code" required/>
            <script>
                const button = document.getElementById('Button_sendCode');
                button.addEventListener('click', () => {
                  if (document.getElementById('user').value == ""){alert('Incorrect leerlingnummer.'); return}
                    fetch('/send_code?userid=' + document.getElementById('user').value, {method: 'POST'})
                        .then(response => response.text())
                        .then(text => alert(text));
                });
            </script>
          </fieldset>
          <div id="i2qefk">
          </div>
          <fieldset id="i1gun">
            <legend id="i8e22j">Selecteer waarop je wilt stemmen:</legend>
            <div id="iy8oeq">
              <button type="submit" id="ifdlg">Verzend stem</button>
              {{!select_vote}}
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
  .flex-desc{
    margin-bottom:55px;
    font-size:1em;
    color:rgba(0, 0, 0, 0.5);
    text-align:center;
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
  }
  #user{
    display:flex;
    margin:0 0 6px 0;
    width:100%;
    height:30px;
    border-radius:5px 5px 5px 5px;
    border:0px solid white;
  }
  #imzij{
    margin:0 0 6px 0;
    display:flex;
    flex-direction:row;
    justify-content:flex-start;
    align-items:flex-start;
    width:100%;
    height:30px;
    border:0px solid white;
    border-radius:5px 5px 5px 5px;
  }
  #iprpw-2{
    margin:0 0 10px 0;
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
    display:flex;
  }
  #i9w0u{
    color:#ffffff;
  }
  #i0b1u{
    color:#ffffff;
  }
  #i8e22j{
    color:#ffffff;
  }
  #ifdlg{
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
    width:150px;
    margin:0 10px 0 0;
    display:block;
  }
  #ih2z2{
    margin:0 0 6px 0;
  }
  #i1gun{
    margin:0 0 6px 0;
  }
  #Button_sendCode{
    border-radius:5px 5px 5px 5px;
    opacity:1;
    border:0px solid white;
    display:block;
    width:110px;
    height:30px;
    margin:0 10px 0 0;
    padding:0px 2.5px 0px 2.5px;
    background-repeat:repeat;
    background-position:left top;
    background-attachment:scroll;
    background-size:auto;
    background-image:linear-gradient(#ffffff 0%, #ffffff 100%);
  }
  #iy8oeq{
    height:30px;
    display:flex;
  }
  #Button_sendCode:active{
    box-shadow:0 0 5px 0 black;
  }
  #ifdlg:active{
    box-shadow:0 0 5px 0 black;
  }
  #vote{
    width:100%;
    display:block;
    height:30px;
    background-repeat:repeat;
    background-position:left top;
    background-attachment:scroll;
    background-size:auto;
    background-image:linear-gradient(#ffffff 0%, #ffffff 100%);
    border-radius:5px 5px 5px 5px;
    border:0 solid white;
  }
  #vote:hover{
    background-repeat:repeat;
    background-position:left top;
    background-attachment:scroll;
    background-size:auto;
    background-image:linear-gradient(#ffffff 0%, #ffffff 100%);
  }

input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type=number] {
  -moz-appearance: textfield;
}
</style>