
var selectedCity= document.getElementById("citySelected");
if(selectedCity) {
    var cleanedSelectedCity = JSON.parse(selectedCity.replace(/&#x27;/g, '"'));
}
$(document).ready(function() {
$('#citySelected').multiselect({
buttonClass:'btn btn-warning',
buttonWidth:'260px',
enableFiltering: true,
enableCaseInsensitiveFiltering: true,
includeSelectAllOption: false,
filterPlaceholder:'Search Here..'
});
 $('#citySelected').multiselect('select', cleanedSelectedCity);
});



var selectedSpeciality = document.getElementById("jobtitle");
if(selectedSpeciality) {
    var cleanedSelectedSpeciality = JSON.parse(selectedSpeciality.replace(/&#x27;/g, '"'));
}
$(document).ready(function() {
    $('#jobtitle').multiselect({
        buttonClass:'btn btn-warning',
        buttonWidth:'260px',
        enableFiltering: true,
        enableCaseInsensitiveFiltering: true,
        includeSelectAllOption: false,
        filterPlaceholder:'Search Here..'
    });
     $('#jobtitle').multiselect('select', cleanedSelectedSpeciality);
});