function debounce(func, delay) {
    let timer;
    function showIndicator() {
        const indicator = document.getElementById('saving-indicator');
        if (indicator) {
            indicator.style.display = 'block'; // Show the indicator
        }
    }

    function hideIndicator() {
        const indicator = document.getElementById('saving-indicator');
        if (indicator) {
            indicator.style.display = 'none'; // Hide the indicator
        }
    }
    return function (...args) {
        showIndicator();
        clearTimeout(timer);
        timer = setTimeout(() => {
            func.apply(this, args)
            hideIndicator();
        }, delay);
    };
}

const DEBUG = false;

function debugLog(...args) {
  if (DEBUG) {
    console.log(...args);
  }
}

function calculateCharacterLevel(experience) {
    let level = 1;  
    const xpThresholds = [0, 1000, 2000, 3000, 4000, 5000, 6000, 8000, 10000, 12000, 15000, 18000, 21000, 25000, 30000, 35000, 40000, 45000, 50000, 60000];
    
    for (let i = 0; i < xpThresholds.length; i++) {
        if (experience >= xpThresholds[i]) {
            level = i + 1;  
        }
    }
    return level;
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
    checkbox.addEventListener('change', (event) => {
        updateSkills();
        updateSelectedSkills(event) 
    });
});

let previousSelectedSkills = []; 


function updateSelectedSkills(event) {
    const selectedSkills = [];
    const checkboxes = document.querySelectorAll('.skill-trained-checkbox:checked'); 
    checkboxes.forEach(checkbox => {
        selectedSkills.push(checkbox.dataset.skill);  
    });

    console.log("selectedSkills:", selectedSkills);

    const formData = new FormData();
    formData.append('character_id', character_id); 
    formData.append('added_skills', JSON.stringify(selectedSkills)); 

    fetch('/save_selected_skills/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log("Data saved:", data);
        previousSelectedSkills = selectedSkills;  
    })
    .catch(error => {
        console.error("Error:", error);
    });
}


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
            senseBonusField.value = skillMod; 
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

document.getElementById('id_xp').addEventListener('input', function() {
    const xpValue = parseInt(this.value) || 0;  
    const characterLevel = calculateCharacterLevel(xpValue);  
    document.getElementById('level').value = characterLevel;  
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
    formData.append('character_id', character_id);

   
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
    const debouncedSendData = debounce(sendData,2000);
    form.querySelectorAll('input, select, textarea').forEach(input => {
        input.addEventListener('change', debouncedSendData);  
    });
});

document.addEventListener("DOMContentLoaded", () => {
    console.log("Script loaded!");
    updateAbilityDependencies();  
    const xpInput = document.getElementById('id_xp');
    if (xpInput) {
        const xpValue = parseInt(xpInput.value) || 0; 
        const characterLevel = calculateCharacterLevel(xpValue);
        document.getElementById('level').value = characterLevel;  
    }
    const abilityInputs = document.querySelectorAll('.ability-input');
    abilityInputs.forEach(input => {
        input.addEventListener('input', (event) => {
            updateModifiers();
        });
    });
    poll();
});

function collectCheckboxStates() {
    const checkboxStates = {};
    document.querySelectorAll('.skill-trained-checkbox').forEach(checkbox => {
        checkboxStates[checkbox.dataset.skill] = checkbox.checked;
    });
    return checkboxStates;
}


let last_updated_at = "";
function poll() {
    const char_id = document.getElementById('char-id').getAttribute('data-char-id');
    const selectedSkills = collectCheckboxStates();  

    $.ajax({
        url: "/long_poll/" + char_id,
        method: "GET",
        data: {
            last_updated_at: last_updated_at,
        },
        success: function(response) {
            if (response.status === "Success") {
                last_updated_at = response.updated_at;
                console.log(last_updated_at);

                updateToNewData(response.new_data);
            }
            setTimeout(poll, 700);
        },
        error: function() {
            setTimeout(poll, 5000);
        }
    });
}


function updateToNewData(new_data) {
    updateToNewAbilites(new_data)
    updateToNewDefenses(new_data)
    updateToNewCharacterBase(new_data)
    updateToNewSkills(new_data)  
}

function updateToNewSkills(new_data) {
    const selected_skills = new_data.trained_skills; 
    const skillValues = Object.values(selected_skills);
    skillValues.forEach((value) => {
        const skill = value;
        const skillCheckbox = document.getElementById(`checkbox-${skill}`);
        if (skillCheckbox) {
            skillCheckbox.checked = true;
            if (skillCheckbox.disabled) {
                skillCheckbox.disabled = false;
            }
        } 
    });

    const allCheckboxes = document.querySelectorAll('input[type="checkbox"]');
    allCheckboxes.forEach((checkbox) => {
        const skillName = checkbox.id.replace('checkbox-', ''); 
        if (checkbox.checked && !skillValues.includes(skillName)) {
            checkbox.checked = false; 
        }
    });
    updateSkills()
}


function updateToNewAbilites(new_data){
    abilities = new_data.abilities;
    ability_data = new_data.ability_data;
    abilities.forEach(function (ability) {
        const abilityElement = document.getElementById(ability);

        if (abilityElement && ability_data[ability] !== undefined) {
            abilityElement.value = ability_data[ability];
        }
    });
    updateAbilityDependencies();

}

function updateToNewDefenses(new_data){
    defenses = new_data.defenses;

    ac = document.getElementById("id_armor_coefficient").value = defenses.armor_coefficient;;
    fortitude = document.getElementById("id_fortitude").value = defenses.fortitude;;
    reflex = document.getElementById("id_reflex").value = defenses.reflex;;
    will = document.getElementById("id_will").value = defenses.will;;
}

function updateToNewCharacterBase(new_data){
    const character = new_data.character;

    document.getElementById("id_name").value = character.name;
    document.getElementById("id_char_class").value = character.char_class;
    document.getElementById("id_race").value = character.race;
    document.getElementById("id_xp").value = character.xp;
    document.getElementById("id_size").value = character.size;
    document.getElementById("id_gender").value = character.gender;
    document.getElementById("id_height").value = character.height;
    document.getElementById("id_weight").value = character.weight;
    document.getElementById("id_alignment").value = character.alignment;
    document.getElementById("id_deity").value = character.deity;
    document.getElementById("id_speed").value = character.speed;
    document.getElementById("id_action_points").value = character.action_points;
}


function toggleExtraFields(id) {
    const element = document.getElementById(id);
    if (element.style.display === "none") {
        element.style.display = "block";
    } else {
        element.style.display = "none";
    }
}
