var foodify = {version: "1.0.0"};

(function () {
	"use strict";

    foodify._hideProgressBar = function() {
        $("#progress").hide();
    };

    foodify._showError = function(msg) {
        $("#error_p").html(msg);
        $("#error_div").show();
    };


    foodify._updateRandomComment = function(comments) {
        var random_comment = foodify._getRandomComment(comments);
        $("#random_subreddit").html(random_comment.subreddit + ": "  + random_comment.karma);
        $("#comment_span").html(random_comment.comment);
    };

     foodify._updateLinkField = function(username) {
        $("#karmawhore_link").val("http://www.karmawho.re/?user=" + username);
     };

    foodify._setUserFields = function(username, comments) {
        foodify._updateLinkField(username);
        foodify._updateUsername(username);
        foodify._updateRandomComment(comments);
    };

    foodify._moveCardsToTop = function() {
        var new_top = $('#searchbox').position().top + $('#searchbox').height() + 10;
        $('.card_container').animate({'opacity': 'show', 'top': new_top});
        $('.card_container').css('display', 'table');
    };

	/**
	* Invoked after user comments have been loaded.
	*
	* @param comments A list of comment objects or null.
	**/
    foodify._onCommentsLoaded = function(comments) {
        foodify._hideProgressBar();

        if (comments === null) {
            foodify._showError('Could not retrieve user comments');
        }
        else if (comments.length === 0) {
            foodify._showError('This user never made any comments');
        }
        else {

            foodify._drawCommentCloud('#card_wordcloud svg', comments);

            var username = comments[0].author;

            foodify._setUserFields(username, comments);
            foodify._moveCardsToTop();
        }
    };

    foodify._moveSearchboxToTop = function() {
        var topx = $("#header").height();
        $("#searchbox").animate({top:topx + 120}, 300, 'swing', function() {
            $("#error_div").hide();
            $("#progress").show();
        });
    };

    foodify._startSearch = function() {
        foodify._resetCards();
        foodify._moveSearchboxToTop();
    };


    foodify._resetCards = function() {
        $('.card_container').attr('style','');
        $('#card_wordcloud svg g').remove();
    };

    foodify._setUserInputField = function(username) {
        $("#input_username").val(username);
    };


    foodify._drawCommentCloud = function(div, comments) {
        var comment_strings = splib.project(comments, 'comment');
        var comment_string = comment_strings.join(' ');
        var simplified_comment_string = foodify._simplifyText(comment_string);
        foodify._drawWordcloud(simplified_comment_string, div);
    };

    foodify._wordScale = function(frequency, max){
        return 80 * frequency / max;
    };

    foodify._drawWordcloud = function(tags, div) {
        var words = splib.project(tags, 'key');
        var frequency = splib.project(tags, 'value');
        var max = Math.max.apply(0, frequency);

        d3.layout.cloud().size([800, 400])
            .words(tags.map(function(d, j) {
                return {text: d.key, size: d.value};
            }))
            .padding(5)
            .rotate(function() { return ~~(Math.random() * 2) * 90; })
            .font("Impact")
            .fontSize(function(d){ return foodify._wordScale(d.size, max); })
            .on("end", function(words) {foodify._drawFinalWordCloud(words, div);})
            .start();
    };

    foodify._drawFinalWordCloud = function(words, div) {
        var fill = d3.scale.category20();

        d3.select(div)
            .attr("width", 800)
            .attr("height", 380)
            //.attr("style", "background-color:white")
        .append("g")
          .attr("transform", "translate(400,200)")
        .selectAll("text")
          .data(words)
        .enter().append("text")
            .style("font-size", function(d) { return d.size + "px"; })
            .style("font-family", "Impact")
            .style("fill", function(d, i) { return fill(i); })
            .attr("text-anchor", "middle")
            .attr("transform", function(d) {
                 return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
            })
        .text(function(d) { return d.text; });
    }

    foodify._simplifyText = function(text) {
        var tags = {};
        var cases = {};
        var wordSeparators = /[\s\u3031-\u3035\u309b\u309c\u30a0\u30fc\uff70]+/g;
        text.split(wordSeparators).forEach(function(word) {

            word = word.replace(/\W/g, '');

            if (word === "") {
                return;
            }

            if (stopwords.indexOf(word.toLowerCase()) != -1) {
                return;
            }

            cases[word.toLowerCase()] = word;
            tags[word = word.toLowerCase()] = (tags[word] || 0) + 1;
        });

        tags = d3.entries(tags).sort(function(a, b) { return b.value - a.value; });
        tags.forEach(function(d) { d.key = cases[d.key]; });
        tags = tags.splice(0, 50);

        return tags;
    }







})();
