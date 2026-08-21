const invalid_int_error_msg = "Error: Please enter a valid integer.";
const positive_num = new RegExp("^[0-9]+$");

function positive_num_ErrorIndicator(field_name) {
    return "Error: Please enter a positive integer value for " + field_name + ".";
}

function zero_ErrorIndicator(field_name) {
    return "Error: " + field_name + " cannot be Zero.";
}

function createFullscreenImg(img_url, alt_txt, viewport, media_id) {
    const img = document.createElement('img');

    img.src = img_url;
    img.alt = alt_txt;
    img.setAttribute('area-label', alt_txt);
    
    img.id = media_id;
    img.style.setProperty('--w_start', '200px');
    img.style.setProperty('--h_start', '200px');
    img.style.setProperty('--w_end', '300px');
    img.style.setProperty('--h_end', '300px');
    img.classList.add('pfpic','br8','scale-in-anim');

    // Default bubbling listener to stop parent click
    img.addEventListener('click', stopParentEvents);
    viewport.classList.add('center');
    viewport.appendChild(img);
}

function createFullscreenVideo(vid_url, alt_txt, viewport, media_id) {
    const video = document.createElement('video');

    video.src = vid_url;
    video.setAttribute('aria-label', alt_txt);
    video.controls = true; // Shows play, pause, volume, and fullscreen buttons
    video.autoplay = true; // Start playing immediately on page load

    // 3. Performance & Mobile Optimizations
    video.preload = 'metadata'; // Only downloads video duration/dimensions to save user data
    video.playsInline = true; // Prevents iPhones from forcing fullscreen playback automatically
    
    video.id = media_id;
    video.style.setProperty('--w_start', '700px');
    video.style.setProperty('--h_start', 'auto');
    video.style.setProperty('--w_end', '800px');
    video.style.setProperty('--h_end', 'auto');
    video.classList.add('pfpic','br8','scale-in-anim');

    // Default bubbling listener to stop parent click
    video.addEventListener('click', stopParentEvents);
    viewport.classList.add('center');
    viewport.appendChild(video);
}

function createFullscreenPdf(pdf_url, viewport, page_indicator) {
    pdfjsLib.GlobalWorkerOptions.workerSrc = 
    "https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.worker.min.js";

    pdfjsLib.getDocument(pdf_url).promise.then(function(pdf) {
        page_indicator.textContent = `Page 1 / ${pdf.numPages}`;

        // Recursive function to load pages one after another
        function renderPage(pageNum) {
            if(pageNum > pdf.numPages) return; // Exit when all pages are done

            pdf.getPage(pageNum).then(function(page) {
                // 1. Create the standard visual canvas
                const canvas = document.createElement('canvas');
                canvas.classList.add('pdf-page');
                canvas.addEventListener('click', stopParentEvents);
                viewport.appendChild(canvas);
                
                const context = canvas.getContext('2d');
                const pageViewport = page.getViewport({'scale': 1}); // Kept scale at 1.5 for steady rendering performance
                canvas.height = pageViewport.height;
                canvas.width = pageViewport.width;

                // 2. Render the page visuals
                page.render({canvasContext: context, viewport: pageViewport}).promise.then(function(){
                    renderPage(pageNum+1);
                });
            });
        }

        renderPage(1);

        viewport.onscroll = function() {
            const pages = viewport.getElementsByClassName('pdf-page');
            for(let i = 0; i < pages.length; i++) {
                if(pages[i].offsetTop + (pages[i].offsetHeight/2) > viewport.scrollTop) {
                    page_indicator.textContent = `Page ${i+1} / ${pdf.numPages}`;
                    break;
                }
            }
        }
    });
}

function close_fullscreen() {
    fullscreen = document.getElementById('black-fullscreen');
    fs_display_media = document.getElementById('fs-display-media');

    // 1. Swap the classes to trigger the fadeOut animation
    fullscreen.classList.remove('visible');
    fullscreen.classList.add('close');
    if(fs_display_media) {
        fs_display_media.classList.remove('scale-in-anim');
        fs_display_media.classList.add('scale-out-anim');
    }

    // 2. Wait 300ms for the animation, then hide it completely
    setTimeout(()=> {
        fullscreen.classList.remove('close'); // Reverts back to display: none
        if(fs_display_media)
            fs_display_media.classList.remove('scale-out-anim');
        fullscreen.textContent = '';
    }, 100);
}

// Prevents closing the parent events when clicking the child itself
function stopParentEvents(event) {
    event.stopPropagation(); // Stops the click from bubbling up to parent elements
}

function displayMediaFullscreen(url, person_name, media_type, alt_txt, template_id) {
    const fullscreen = document.getElementById('black-fullscreen');
    const template = document.getElementById(template_id);
    const clone = template.content.cloneNode(template);
    fullscreen.textContent = '';
    fullscreen.appendChild(clone);

    const title_ele = document.getElementById('media-head-title');
    const file_title = alt_txt + ' - ' + person_name;
    title_ele.textContent = file_title;

    const viewport = document.getElementById('bfs-viewport');
    // this id supports for animating the displayed media on opening and closing on fullscreen
    const media_id = 'fs-display-media';
    
    if(media_type=='img') {
        createFullscreenImg(url, alt_txt, viewport, media_id);
    }
    else if(media_type=='video') {
        createFullscreenVideo(url, alt_txt, viewport, media_id);
    }
    else if(media_type=='pdf') {
        const page_indicator = document.getElementById('page-indicator');
        const download_hyperlink = document.getElementById('media-download');
        const openinnewtab_hyperlink = document.getElementById('media-openinnewtab');
        download_hyperlink.href = url;
        openinnewtab_hyperlink.href = url;
        createFullscreenPdf(url, viewport, page_indicator);
    }
    
    fullscreen.classList.add('visible');
}

// Display Profile Picture as Fullscreen
function dmfs_pfpic(img_url, person_name) {
    const media_type = 'img';
    const alt_txt = 'Profile Picture';
    const template_id = 'temp-imgvid';
    displayMediaFullscreen(img_url, person_name, media_type, alt_txt, template_id);
}

// Display Interview Video as Fullscreen
function dmfs_intvid(vid_url, person_name) {
    const media_type = 'video';
    const alt_txt = 'Interview Video';
    const template_id = 'temp-imgvid';
    displayMediaFullscreen(vid_url, person_name, media_type, alt_txt, template_id);
}

// Display Resume as Fullscreen
function dmfs_resume(resume_url, person_name) {
    const media_type = 'pdf';
    const alt_txt = 'Resume';
    const template_id = 'temp-pdf';
    displayMediaFullscreen(resume_url, person_name, media_type, alt_txt, template_id);
}