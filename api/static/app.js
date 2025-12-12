const searchInput = document.getElementById('searchInput');
const searchBtn = document.getElementById('searchBtn');
const resultsContainer = document.getElementById('results');
const loading = document.getElementById('loading');
const player = document.getElementById('player');
const audioPlayer = document.getElementById('audioPlayer');
const playPauseBtn = document.getElementById('playPauseBtn');
const playIcon = document.getElementById('playIcon');
const pauseIcon = document.getElementById('pauseIcon');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const progressBar = document.getElementById('progressBar');
const currentTimeEl = document.getElementById('currentTime');
const totalTimeEl = document.getElementById('totalTime');
const volumeBar = document.getElementById('volumeBar');
const playerThumbnail = document.getElementById('playerThumbnail');
const playerTitle = document.getElementById('playerTitle');
const playerChannel = document.getElementById('playerChannel');
const playlistContainer = document.getElementById('playlist');
const playlistItems = document.getElementById('playlistItems');

let playlist = [];
let currentIndex = 0;
let isPlaying = false;

function formatDuration(seconds) {
    if (!seconds) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

async function search(query) {
    loading.classList.remove('hidden');
    resultsContainer.innerHTML = '';
    
    try {
        const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        
        if (data.error) {
            resultsContainer.innerHTML = `<p style="text-align:center;color:#ff6b6b;">Error: ${data.error}</p>`;
            return;
        }
        
        if (data.results.length === 0) {
            resultsContainer.innerHTML = '<p style="text-align:center;">No results found</p>';
            return;
        }
        
        data.results.forEach((item, index) => {
            const card = document.createElement('div');
            card.className = 'result-card';
            card.innerHTML = `
                <img src="${item.thumbnail}" alt="${item.title}" loading="lazy">
                <div class="card-info">
                    <h4>${item.title}</h4>
                    <p>${item.channel}</p>
                    <span class="duration">${formatDuration(item.duration)}</span>
                </div>
            `;
            card.onclick = () => playTrack(item, data.results);
            resultsContainer.appendChild(card);
        });
    } catch (error) {
        resultsContainer.innerHTML = `<p style="text-align:center;color:#ff6b6b;">Error: ${error.message}</p>`;
    } finally {
        loading.classList.add('hidden');
    }
}

async function playTrack(track, tracks = null) {
    if (tracks) {
        playlist = tracks;
        currentIndex = tracks.findIndex(t => t.id === track.id);
        updatePlaylist();
        playlistContainer.classList.remove('hidden');
    }
    
    player.classList.remove('hidden');
    playerThumbnail.src = track.thumbnail;
    playerTitle.textContent = track.title;
    playerChannel.textContent = track.channel;
    
    loading.classList.remove('hidden');
    
    try {
        const response = await fetch(`/api/stream/${track.id}`);
        const data = await response.json();
        
        if (data.error) {
            alert('Error loading track: ' + data.error);
            loading.classList.add('hidden');
            return;
        }
        
        audioPlayer.src = data.url;
        audioPlayer.play();
        isPlaying = true;
        updatePlayPauseBtn();
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        loading.classList.add('hidden');
    }
}

function updatePlayPauseBtn() {
    if (isPlaying) {
        playIcon.classList.add('hidden');
        pauseIcon.classList.remove('hidden');
    } else {
        playIcon.classList.remove('hidden');
        pauseIcon.classList.add('hidden');
    }
}

function updatePlaylist() {
    playlistItems.innerHTML = '';
    playlist.forEach((item, index) => {
        const el = document.createElement('div');
        el.className = `playlist-item ${index === currentIndex ? 'active' : ''}`;
        el.innerHTML = `
            <img src="${item.thumbnail}" alt="${item.title}">
            <div class="item-info">
                <h5>${item.title}</h5>
                <p>${item.channel}</p>
            </div>
        `;
        el.onclick = () => {
            currentIndex = index;
            playTrack(item);
            updatePlaylist();
        };
        playlistItems.appendChild(el);
    });
}

searchBtn.onclick = () => {
    const query = searchInput.value.trim();
    if (query) search(query);
};

searchInput.onkeypress = (e) => {
    if (e.key === 'Enter') {
        const query = searchInput.value.trim();
        if (query) search(query);
    }
};

playPauseBtn.onclick = () => {
    if (audioPlayer.src) {
        if (isPlaying) {
            audioPlayer.pause();
        } else {
            audioPlayer.play();
        }
        isPlaying = !isPlaying;
        updatePlayPauseBtn();
    }
};

prevBtn.onclick = () => {
    if (playlist.length > 0 && currentIndex > 0) {
        currentIndex--;
        playTrack(playlist[currentIndex]);
        updatePlaylist();
    }
};

nextBtn.onclick = () => {
    if (playlist.length > 0 && currentIndex < playlist.length - 1) {
        currentIndex++;
        playTrack(playlist[currentIndex]);
        updatePlaylist();
    }
};

audioPlayer.ontimeupdate = () => {
    if (audioPlayer.duration) {
        const progress = (audioPlayer.currentTime / audioPlayer.duration) * 100;
        progressBar.value = progress;
        currentTimeEl.textContent = formatDuration(audioPlayer.currentTime);
    }
};

audioPlayer.onloadedmetadata = () => {
    totalTimeEl.textContent = formatDuration(audioPlayer.duration);
};

audioPlayer.onended = () => {
    if (currentIndex < playlist.length - 1) {
        currentIndex++;
        playTrack(playlist[currentIndex]);
        updatePlaylist();
    } else {
        isPlaying = false;
        updatePlayPauseBtn();
    }
};

progressBar.oninput = () => {
    if (audioPlayer.duration) {
        audioPlayer.currentTime = (progressBar.value / 100) * audioPlayer.duration;
    }
};

volumeBar.oninput = () => {
    audioPlayer.volume = volumeBar.value / 100;
};

audioPlayer.volume = 1;
