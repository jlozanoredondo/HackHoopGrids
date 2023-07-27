$(document).ready(function () {
    function formatState(state) {
        if (!state.id) { return state.text; }
        var $state = $(
            '<span><img src="' + $(state.element).data('image') + '" class="img-flag" /> ' + state.text + '</span>'
        );
        return $state;
    };
    function formatStateSelection(state) {
        if (!state.id) { return state.text; }
        var $state = $(
            '<span><img src="' + $(state.element).data('image') + '" class="img-flag" /> ' + state.text + '</span>'
        );
        return $state;
    };

    $('.team-select').select2({
        theme: 'bootstrap-5',
        templateResult: formatState,
        templateSelection: formatStateSelection
    });

    var $team1 = $('#team1');
    var $team2 = $('#team2');
    var team1Id = $team1.val();
    var team2Id = $team2.val();

    if (team1Id) {
        $team2.find('option[value=' + team1Id + ']').prop('disabled', true);
    }
    if (team2Id) {
        $team1.find('option[value=' + team2Id + ']').prop('disabled', true);
    }

    $team1.add($team2).on('change', function () {
        var team1Id = $team1.val();
        var team2Id = $team2.val();

        $team1.add($team2).find('option').prop('disabled', false);

        if (team1Id) {
            $team2.find('option[value=' + team1Id + ']').prop('disabled', true);
        }
        if (team2Id) {
            $team1.find('option[value=' + team2Id + ']').prop('disabled', true);
        }

        // Submit the form automatically when both selects have values
        if (team1Id && team2Id) {
            $(this).closest('form').submit();
        }

        $team1.add($team2).trigger('change.select2');
    });

});