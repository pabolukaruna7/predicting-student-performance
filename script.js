script_js = 
$(document).ready(function() {
    $('#prediction-form').submit(function(event) {
        event.preventDefault();
        
        let formData = {
            gender: $('#gender').val(),
            study_hours: $('#study_hours').val(),
            attendance: $('#attendance').val(),
            past_exam_scores: $('#past_exam_scores').val(),
            parental_education: $('#parental_education').val(),
            internet_access: $('#internet_access').val(),
            extracurricular: $('#extracurricular').val()
        };
        
        $.ajax({
            url: '/predict',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(formData),
            success: function(response) {
                $('#result').text(response.result || 'Error occurred');
            }
        });
    });
});
