// Get the gear icon button
const gearIconButton = document.querySelector('.btn-outline-success');


const getSettingFromServer = async () => {
    const response = await fetch('/get_setting');
    const data = await response.json();
    return data
}
// Add a click event listener
if (gearIconButton) {
    gearIconButton.addEventListener('click', async () => {
        const setting = await getSettingFromServer();
        // Create the settings menu div
        const settingsMenu = document.createElement('div');
        settingsMenu.classList.add('card')
        settingsMenu.classList.add('settings-menu');
        // Add your HTML content for the settings menu here
        settingsMenu.innerHTML = `
        <div class="container">
            <h3>Settings</h3>
            <form method="post" action="/setting">
                <div class="mb-3">
                    <label for="ai-model" class="form-label">Stock prediction model</label>
                    <select name="model" class="form-select" aria-label="Default select example" required>
                        <option value="GPT-4" ${setting.setting.brain === '' || setting.setting.brain === 'GPT-4' ? 'selected' : ''}>GPT-4</option>
                        <option value="claude" ${setting.setting.brain === 'claude' ? 'selected' : ''}>Claude-Opus</option>
                    </select>
                </div>
                <div class="mb-3">
                    <label for="api" class="form-label">API key</label>
                    <input name="api" type="text" class="form-control" id="api" value="${setting.setting.api}" placeholder="Enter your API key" required>
                </div>
                <button type="submit" class="btn btn-primary">Save</button>
                <a href="" class="btn btn-secondary float-end">Go Back</a>
            </form>
        </div>
    `;

        // Create the background overlay div
        const overlay = document.createElement('div');
        overlay.classList.add('overlay');

        // Append the settings menu and overlay to the body
        document.body.appendChild(settingsMenu);
        document.body.appendChild(overlay);
    });
}