async function unblock(profileId) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    await fetch(`/block/${profileId}`, {
        method: 'DELETE',
        headers: { 'X-CSRFToken': csrftoken },
        mode: 'same-origin'
    })

    window.location.replace('/block')
}

async function block(profileId) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    await fetch(`/block/${profileId}`, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken },
        mode: 'same-origin'
    })

    window.location.replace('/block')
}