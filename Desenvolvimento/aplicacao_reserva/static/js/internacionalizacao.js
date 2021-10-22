

function Translate() { 
    //initialization    
    this.init =  function(attribute, lng){
        this.attribute = attribute;
        this.lng = lng;    
    }

    //translate 
    this.process = function(){
                _self = this;
                var xrhFile = new XMLHttpRequest();
                //load content data 
                xrhFile.open("GET", "../static/languages/"+this.lng+".json", false);
                xrhFile.onreadystatechange = function (){
                    if(xrhFile.readyState === 4){
                        if(xrhFile.status === 200 || xrhFile.status == 0){
                            var LngObject = JSON.parse(xrhFile.responseText);
                            console.log(LngObject["name1"]);
                            var allDom = document.getElementsByTagName("*");
                            for(var i =0; i < allDom.length; i++){
                                var elem = allDom[i];
                                var key = elem.getAttribute(_self.attribute);
                                 
                                if(key != null) {
                                     console.log(key);
                                     elem.innerHTML = LngObject[key]  ;
                                }
                            }
                        }
                    }
                }
                xrhFile.send();
    }
}

  var down_1 = document.getElementById('pt_Br');
  var down_2 = document.getElementById('en_us');

  function load(){
    var translate = new Translate();
    var currentLng = 'pt';
    var attributeName = 'data-tag';
    translate.init(attributeName, currentLng);
    translate.process(); 
  }

  function pt_Br() {
    var translate = new Translate();
    var currentLng = 'pt';
    var attributeName = 'data-tag';
    translate.init(attributeName, currentLng);
    translate.process(); 
  }

  function en_us() {
    var translate = new Translate();
    var currentLng = 'en';
    var attributeName = 'data-tag';
    translate.init(attributeName, currentLng);
    translate.process(); 
  }