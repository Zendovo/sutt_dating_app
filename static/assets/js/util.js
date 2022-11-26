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

async function accept(requestId) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    await fetch(`/request/${requestId}`, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken },
        mode: 'same-origin'
    })

    window.location.replace('/chat')
}

async function decline(requestId) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    await fetch(`/request/${requestId}`, {
        method: 'DELETE',
        headers: { 'X-CSRFToken': csrftoken },
        mode: 'same-origin'
    })

    window.location.replace('/chat')
}

function openRequestModal(profileId) {
    var modal = new bootstrap.Modal(document.getElementById('chatRequestModal'))
    document.getElementById('chatRequestModalBtn').setAttribute('onclick', `sendRequest(${profileId})`)
    modal.show()
}

async function sendRequest(profileId) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    formData = new FormData()
    formData.append("profile_id", profileId)
    formData.append("message", document.getElementById('chatRequestMessage').value)
    await fetch(`/request/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken },
        mode: 'same-origin',
        body: formData
    })

    window.location.replace('/')
}

function openReportModal(profileId) {
    var modal = new bootstrap.Modal(document.getElementById('reportModal'))
    document.getElementById('reportModalBtn').setAttribute('onclick', `sendReport(${profileId})`)
    modal.show()
}

async function sendReport(profileId) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    formData = new FormData()
    formData.append("profile_id", profileId)
    formData.append("message", document.getElementById('reportMessage').value)
    await fetch(`/report/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken },
        mode: 'same-origin',
        body: formData
    })

    window.location.replace('/')
}

function openDeleteAccountModal(reportId) {
    var modal = new bootstrap.Modal(document.getElementById('deleteAccountModal'))
    document.getElementById('deleteAccountModalBtn').setAttribute('onclick', `deleteAccount(${reportId})`)
    modal.show()
}

async function deleteAccount(reportId) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    formData = new FormData()
    formData.append("action", 'delete_account')
    await fetch(`/mod_reports/${reportId}`, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken },
        mode: 'same-origin',
        body: formData
    })

    window.location.replace('/mod_reports')
}

async function deleteReport(reportId) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    await fetch(`/mod_reports/${reportId}`, {
        method: 'DELETE',
        headers: { 'X-CSRFToken': csrftoken },
        mode: 'same-origin',
    })

    window.location.replace('/mod_reports')
}