$(document).ready(function() {
    $("#reserv").find("[id^='2tab']").hide(); // Hide all content
    $("#title_reserv li:first").attr("id","current"); // Activate the first tab
    $("#reserv #2tab1").fadeIn(); // Show first tab's content
    $('#title_reserv a').click(function(e) {
        e.preventDefault();
        if ($(this).closest("li").attr("id") == "current"){ //detection for current tab
         return;
        }
        else{
          $("#reserv").find("[id^='2tab']").hide(); // Hide all content
          $("#title_reserv li").attr("id",""); //Reset id's
          $(this).parent().attr("id","current"); // Activate this
          $('#' + $(this).attr('name')).fadeIn(); // Show content for the current tab
        }
    });
});