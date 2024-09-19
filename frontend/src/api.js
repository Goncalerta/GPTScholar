import axios from "axios";

const URL = process.env.REACT_APP_BACKEND_URL;

function getConfig(controller) {
    return {
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        signal: controller.signal,
    };
}

function getEndpoint(URL, route) {
    return `http://${URL}/api/${route}`;
}

async function getBackend(path, content, controller) {
    const options = getConfig(controller);
    const endpoint = getEndpoint(URL, path);

    return axios.get(endpoint, {...content}, options);
}

async function postBackend(path, content, controller) {
    const options = getConfig(controller);
    const endpoint = getEndpoint(URL, path);

    return axios.post(endpoint, {...content}, options);
}

async function ping(controller) {
    return getBackend("ping", {}, controller)
        .then(response => response.data.response)
        .catch(err => ({error: err}));
}

async function prompt(text, controller) {
    return postBackend("prompt", {prompt: text}, controller)
        .then(response => response.data.response)
        .catch(err => ({error: err}));
}

const api = {
    prompt,
    ping,
};
export default api;
