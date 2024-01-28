function handle_lookup(event) {
    // Get the value to lookup
    var word = event.target.querySelector("input[type='search']").value
    // Do the lookup
    paling.lookup_word(word)().then((result) => {
        var orig_word = result[0];
        var definitions = result[1];
        console.log(orig_word);
        console.log(definitions);
        show_definitions(orig_word, definitions);
    });
    // Stop the default form action from firing
    event.preventDefault();
}

function handle_show_example(event) {
    // Get the example data from the event target (the link that was clicked on)
    var example_data = event.target.dataset;
    var example_id = example_data['example_id'];
    var example_def = decodeURIComponent(example_data['example_def']);
    var example_text = decodeURIComponent(example_data['example_text']);
    var example_word = decodeURIComponent(example_data['example_word']);
    var example_style = document.querySelector("nav form select").value
    var example_query =
        ((example_style == '') ? '' : example_style + "; ")
        + example_word + " - " + example_def + ", for example '" + example_text + "'";
    // Get the placeholder element for the given example id
    var placeholder = document.querySelector("#exampleholder_" + example_id);
    // Make the placeholder visible
    placeholder.classList.remove('d-none');
    // Get the image representation of the example text
    paling.represent_text(example_query)().then((example_image_data) => {
        // Get the image for the example and update its source to use the returned base64 image
        var img = placeholder.querySelector("img");
        img.src = 'data:image/png;base64,' + example_image_data;
        // Use the result to get the video representation too
        paling.represent_image(example_image_data)().then((example_video_url) => {
            var vid = placeholder.querySelector("video");
            // Set the video's source to the given video url
            vid.src = example_video_url;
            // Start the video playing
            vid.play()
        });
    });
    // Stop the default anchor action from firing
    event.preventDefault();
}

function show_definitions(word, definitions) {
    // Update the placeholders
    document.querySelector("#definitions .word").innerText = word;
    document.querySelector("#definitions .def_count").innerText = definitions.length;
    // Create content for each definition
    var html = '';
    for (d in definitions) {
        var def = definitions[d];
        html += '<li class="py-1">';
        html += '<p class="h5">' + def['definition'] + '</p>';
        html += '<p><span class="wordtype">' + def['partOfSpeech'] + '</span></p>';
        for (e in def['examples']) {
            var eId = d + '_' + e;
            var example = def['examples'][e]
            html += '<div class="py-1">';
                html += '<blockquote class="blockquote">' + example + '</blockquote>';
                // URI encode the example on the link data so that it doesn't mess up the syntax
                html += '<p><a href="#" data-example_id="' + eId
                    + '" data-example_def="' + encodeURIComponent(def['definition'])
                    + '" data-example_text="' + encodeURIComponent(example)
                    + '" data-example_word="' + encodeURIComponent(word)
                    + '">Show Me</a></p>';
                html += '<div id="exampleholder_' + eId + '" class="d-none">';
                    html += '<div class="row align-items-start">';
                        html += '<div class="col">';
                        html += 'Generated Image<br/><img width="240" src="loading.gif" style="vertical-align:baseline"/>';
                        html += '</div>';
                        html += '<div class="col">';
                        html += 'Generated Video<br/><video controls width="240" poster="loading.gif"></video>';
                        html += '</div>';
                    html += '</div>';
                html += '</div>';
            html += '</div>';
        }
        html += "</li>";
    }
    // Update the definitions element on the page
    document.querySelector("#definitions .definitions").innerHTML = html;
    // Register event handlers for each of the link elements we added
    document.querySelectorAll("#definitions .definitions a").forEach(
        (el) => el.addEventListener('click', handle_show_example));
    // Hide the other content and show this one
    show_page("definitions")
}

function show_page(page) {
    // Hide all the pages
    document.querySelector("div.container").classList.add("d-none");
    // Show the given page
    document.querySelector("#" + page).classList.remove("d-none");
    // Don't show the navbar on the home page
    if (page == "home") {
        document.querySelector("nav").classList.add("d-none");
    } else {
        document.querySelector("nav").classList.remove("d-none");
    }
}

document.querySelector("#home form").addEventListener('submit', handle_lookup);
document.querySelector("nav form").addEventListener('submit', handle_lookup);
