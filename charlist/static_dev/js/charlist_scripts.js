function debounce(func, delay) {
    let timer;
    return function (...args) {
        clearTimeout(timer);
        timer = setTimeout(() => func.apply(this, args), delay);
    };
}

const DEBUG = false;

function debugLog(...args) {
  if (DEBUG) {
    console.log(...args);
  }
}

const SKILL_DEPENDENCIES = {
    "acrobatic": "Dexterity",
    "arcana": "Intelligence",
    "athletic": "Strength",
    "bluff": "Charisma",
    "diplomacy": "Charisma",
    "dungeoning": "Wisdom",
    "endurange": "Strength",
    "heal": "Wisdom",
    "history": "Intelligence",
    "insight": "Wisdom",
    "intimidate": "Charisma",
    "nature": "Wisdom",
    "perception": "Wisdom",
    "religion": "Intelligence",
    "stealth": "Dexterity",
    "streetwise": "Charisma",
    "thievery": "Dexterity"
};


function calculateModifier(score) {
    return Math.floor((score - 10) / 2);  
}

document.querySelectorAll('.skill-trained-checkbox').forEach(checkbox => {
    checkbox.addEventListener('change', () => {
        updateSkills(); 
    });
});

function updateSkills() {
    const skillElements = document.querySelectorAll('.skill_value');
    skillElements.forEach(skillElement => {
        const skillName = skillElement.id;
        const dependentAbility = SKILL_DEPENDENCIES[skillName.toLowerCase()];
        const abilityScore = parseInt(document.getElementById(dependentAbility.toLowerCase()).value) || 0;

        const mod = calculateModifier(abilityScore);
        let skillMod = mod;


        const checkbox = document.querySelector(`#checkbox-${skillName}`);
        if (checkbox && checkbox.checked) {
            skillMod += 5;
        }


        skillElement.textContent = skillMod;

        debugLog(`Updated ${skillName}: mod=${skillMod}`);
        const senseBonusField = document.getElementById(`${skillName}-bonus`);
        if (senseBonusField) {
            senseBonusField.value = skillMod;  // Дублируем значение навыка в бонус чувств
        }
    });
}

function updateModifiers() {
    const abilityInputs = document.querySelectorAll('.ability-input');
    abilityInputs.forEach(input => {
        const score = parseInt(input.value) || 0; 
        const abilityId = input.id;  

     
        const mod = calculateModifier(score); 
        const modPlus = mod + 1;  

        
        const modField = document.getElementById(`${abilityId}-mod`);
        const modPlusField = document.getElementById(`${abilityId}-mod-plus`);

        if (modField) modField.value = mod; 
        if (modPlusField) modPlusField.value = modPlus;  

        debugLog(`Updated ${abilityId}: mod=${mod}, modPlus=${modPlus}`);
    });

}

function updateAbilityDependencies(){
    updateModifiers();
    updateSkills();
}

document.querySelectorAll('.ability-input').forEach(input => {
    input.addEventListener('input', () => {
        updateAbilityDependencies();
    });
});


function sendData(event) {
    const form = event.target.closest('form');
    const formName = form ? form.dataset.formName : null;
    const formType = form ? form.dataset.formType : null;  

    if (!formName) {
        console.error("Form name not found!");
        return;
    }


    const formData = new FormData(form);

    formData.append('user', userId);  
    formData.append('session_key', sessionKey);
    formData.append('character_name', character_name);

   
    let url = '';
    if (formType === 'model_form') {
        url = `/save_model_form_data/${formName}/`; 
    } else if (formType === 'handwritten') {
        url = `/save_handwritten_form_data/${formName}/`;  
    } else {
        console.error("Unknown form type");
        return;
    }


    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log("Data saved:", data);
    })
    .catch(error => {
        console.error("Error:", error);
    });
}

function getCSRFToken() {
    return document.cookie.split('; ').find(row => row.startsWith('csrftoken=')).split('=')[1];
}

document.querySelectorAll("form").forEach(form => {
    const debouncedSendData = debounce(sendData, 1000);
    form.querySelectorAll('input, select, textarea').forEach(input => {
        input.addEventListener('change', debouncedSendData);  
    });
});

document.addEventListener("DOMContentLoaded", () => {
    console.log("Script loaded!");
    updateAbilityDependencies();  

    const abilityInputs = document.querySelectorAll('.ability-input');
    abilityInputs.forEach(input => {
        input.addEventListener('input', (event) => {
            updateModifiers();
        });
    });
});


function toggleExtraFields(id) {
    const element = document.getElementById(id);
    if (element.style.display === "none") {
        element.style.display = "block";
    } else {
        element.style.display = "none";
    }
}
