async function processForm(evt) {
    evt.preventDefault();
    let search = $('#search').val();
    const res = await axios.post('/api/search', params = { "search": search })
    handleResponse(res, search);
}

async function clickLink(evt) {
    evt.preventDefault();
    let search = evt.target.innerText;
    const res = await axios.post('/api/search', params = { "search": search })
    handleResponse(res, search);
}

function handleResponse(resp, term) {
    if (resp.data.errors) {
        let errors = resp.data.errors;
        let keys = Object.keys(errors);
        let values = Object.values(errors);

        for (let i = 0; i < keys.length; i++) {
            let parent = $(`#errors`);
            parent.text(`${values[i]}`).css('color', 'red');
        }
    } else {

        $('#errors').text('');
        $('#videosDiv').children().remove();
        $('#searchTermHeading').text(`${term} videos`).addClass('mb-3 mt-3');
        $('#videosDiv').append(`<div data-bs-spy='scroll' id="scrollTechniques" tabindex="0"></div>`);
        $('#scrollTechniques').css("overflow-y", "scroll").css("overflow-x", "hidden").css("height", "65vh").css("position", "relative");
        let items = resp.data.items;
        items.forEach(function (item) {
            let videoId = item.id.videoId;
            let channelTitle = item.snippet.channelTitle;
            let videoTitle = item.snippet.title;
            console.log(videoTitle)
            videoTitle = videoTitle.replace('/', '-');
            console.log(videoTitle);
            $('#scrollTechniques').append(`<div id=${videoId}></div>`);
            $(`#${videoId}`).append(`<div class="card mb-3 border-light" style="width: 90%;">
        <iframe class="card-img-top" width="560" height="315" src="https://www.youtube.com/embed/${videoId}" title="YouTube video player"
                frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen></iframe>
                <div class="card-body">
                <div class='row'>
            <div class='col-9'>
            <h5 class="card-title">${channelTitle}</h5>
            <p class="card-text">${videoTitle}</p>
            </div>
            <div class='col-3'>
            
            <form class="mb-3" method="POST" action="/techniques/${videoId}/${videoTitle}/${channelTitle}">
                            <button class="btn btn-primary">Add to My Techniques</button>
                        </form>
                        
            </div>
            </div>
          </div>
        </div>`)

        })
    }
}

$('#searchForm').on('submit', processForm);

$('.techLink').on('click', clickLink);