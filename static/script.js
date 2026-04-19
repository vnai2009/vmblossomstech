let currentStep = 0;

function nextStep() {
    const steps = document.querySelectorAll(".step");
    steps[currentStep].classList.remove("active");
    currentStep++;
    if (steps[currentStep]) {
        steps[currentStep].classList.add("active");
    }
}