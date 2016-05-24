$(document).ready(function(){

  function askServer(root,callFunc){
    $SCRIPT_ROOT = {{ request.script_root|tojson|safe }};
    $.getJSON($SCRIPT_ROOT + root ,function(data){
    callFunc(data);
    });
  }

  function askServer(root,info,callFunc){
    $SCRIPT_ROOT = {{ request.script_root|tojson|safe }};
    $.getJSON($SCRIPT_ROOT + root ,{
      message: info
    },function(data){
    callFunc(data);
  });
}

  var priting = function(data){
    alert(data.ches);
  }
  askServer('/getutil','Hello!!!!!!!!!!!!!!!!!!!!!!!!',priting);
  /*$SCRIPT_ROOT = {{ request.script_root|tojson|safe }};
  $.getJSON($SCRIPT_ROOT + '/getutil', {
      message: "{{ message }}"
  },function(data){
    alert(data.ches);
  });
  */
  $.getJSON($SCRIPT_ROOT + '/getTopTopics' ,function(data){
    alert(data.ches);
  });

  $("tr").click(function(){
    alert('{{message}}');
    //alert('Something')
    if( typeof $(this).attr('id') !== 'undefined'){
    var iden = "/posting/"+$(this).attr("id");
    //window.document.location =iden;

     window.location.href = iden;
   }
  });

  $('#plus').click(function(){
    $SCRIPT_ROOT = {{ request.script_root|tojson|safe }};
    $.getJSON($SCRIPT_ROOT + '/change', {
        valeur: {{ valeur }} + 10
    });
    window.location.href = '/';
  });
  $('#moins').click(function(){
    $SCRIPT_ROOT = {{ request.script_root|tojson|safe }};
    $.getJSON($SCRIPT_ROOT + '/change', {
        valeur: {{ valeur }} - 10
    });
    window.location.href = '/';
  });
});
