/* Логика управления сценариями фотостудии */

class PhotoStudioApp {
    constructor() {
        this.currentLocation = null;
        this.currentType = null;
        this.uploadedPhoto = null;
        this.currentSlide = 0;

        this.init();
    }

    init() {
        this.showWelcome();
        this.setupEventListeners();
        this.initTour();
    }

    setupEventListeners() {
        // Обработка загрузки файлов
        const fileInput = document.getElementById('photoInput');
        if (fileInput) {
            fileInput.addEventListener('change', (e) => this.handlePhotoUpload(e));
        }

        // Закрытие модального окна по клику на фон
        const modal = document.getElementById('tour-modal');
        if (modal) {
            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.closeTour();
                }
            });
        }
    }

    // Показать приветствие и студию
    showWelcome() {
        this.hideAllSections();
        document.getElementById('welcome-section').classList.remove('hidden');
    }

    // Открыть локацию
    openLocation(location) {
        this.currentLocation = location;
        this.hideAllSections();

        switch (location) {
            case 'portrait':
                this.showPortraitLocation();
                break;
            case 'organizer':
                this.showOrganizerLocation();
                break;
            case 'wedding':
                this.showWeddingLocation();
                break;
            case 'compliment':
                this.showComplimentLocation();
                break;
        }
    }

    // Портретная зона
    showPortraitLocation() {
        const section = document.getElementById('portrait-section');
        document.getElementById('portrait-question').classList.remove('hidden');
        document.getElementById('portrait-tips').classList.add('hidden');
        document.getElementById('portrait-upload').classList.add('hidden');
        document.getElementById('portrait-result').classList.add('hidden');
        section.classList.remove('hidden');
    }

    selectPortraitType(type) {
        this.currentType = type;
        document.getElementById('portrait-question').classList.add('hidden');

        const tipsSection = document.getElementById('portrait-tips');
        const tipsText = document.getElementById('portrait-tips-text');
        tipsText.textContent = MESSAGES.portrait.tips[type];
        tipsSection.classList.remove('hidden');
    }

    showPortraitUpload() {
        document.getElementById('portrait-tips').classList.add('hidden');
        document.getElementById('portrait-upload').classList.remove('hidden');
    }

    // Рабочая зона организатора
    showOrganizerLocation() {
        const section = document.getElementById('organizer-section');
        document.getElementById('organizer-upload').classList.remove('hidden');
        document.getElementById('organizer-result').classList.add('hidden');
        section.classList.remove('hidden');
    }

    // Свадебная локация
    showWeddingLocation() {
        const section = document.getElementById('wedding-section');
        document.getElementById('wedding-question').classList.remove('hidden');
        document.getElementById('wedding-tips').classList.add('hidden');
        document.getElementById('wedding-upload').classList.add('hidden');
        document.getElementById('wedding-result').classList.add('hidden');
        section.classList.remove('hidden');
    }

    selectWeddingType(type) {
        this.currentType = type;
        document.getElementById('wedding-question').classList.add('hidden');

        const tipsSection = document.getElementById('wedding-tips');
        const tipsText = document.getElementById('wedding-tips-text');
        tipsText.textContent = MESSAGES.wedding.tips[type];
        tipsSection.classList.remove('hidden');
    }

    showWeddingUpload() {
        document.getElementById('wedding-tips').classList.add('hidden');
        document.getElementById('wedding-upload').classList.remove('hidden');
    }

    // Зона комплиментов
    showComplimentLocation() {
        const section = document.getElementById('compliment-section');
        document.getElementById('compliment-upload').classList.remove('hidden');
        document.getElementById('compliment-result').classList.add('hidden');
        section.classList.remove('hidden');
    }

    // Обработка загрузки фото
    handlePhotoUpload(event) {
        const file = event.target.files[0];
        if (!file || !file.type.startsWith('image/')) {
            alert(MESSAGES.common.needPhoto);
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            this.uploadedPhoto = e.target.result;
            this.showResult();
        };
        reader.readAsDataURL(file);
    }

    // Показать результат с комплиментом
    showResult() {
        let compliment;
        let resultSection;

        switch (this.currentLocation) {
            case 'portrait':
                compliment = getRandomCompliment(MESSAGES.portrait.compliments[this.currentType]);
                resultSection = 'portrait-result';
                document.getElementById('portrait-upload').classList.add('hidden');
                document.getElementById('portrait-photo-preview').src = this.uploadedPhoto;
                document.getElementById('portrait-compliment-text').textContent = compliment;
                break;

            case 'organizer':
                compliment = getRandomCompliment(MESSAGES.organizer.compliments);
                resultSection = 'organizer-result';
                document.getElementById('organizer-upload').classList.add('hidden');
                document.getElementById('organizer-photo-preview').src = this.uploadedPhoto;
                document.getElementById('organizer-compliment-text').textContent = compliment;
                break;

            case 'wedding':
                compliment = getRandomCompliment(MESSAGES.wedding.compliments);
                resultSection = 'wedding-result';
                document.getElementById('wedding-upload').classList.add('hidden');
                document.getElementById('wedding-photo-preview').src = this.uploadedPhoto;
                document.getElementById('wedding-compliment-text').textContent = compliment;
                break;

            case 'compliment':
                compliment = getRandomCompliment(MESSAGES.compliment.compliments);
                resultSection = 'compliment-result';
                document.getElementById('compliment-upload').classList.add('hidden');
                document.getElementById('compliment-photo-preview').src = this.uploadedPhoto;
                document.getElementById('compliment-compliment-text').textContent = compliment;
                break;
        }

        document.getElementById(resultSection).classList.remove('hidden');
    }

    // Триггер выбора файла
    triggerFileUpload() {
        document.getElementById('photoInput').click();
    }

    // Скрыть все секции
    hideAllSections() {
        const sections = document.querySelectorAll('.content-section');
        sections.forEach(section => section.classList.add('hidden'));
    }

    // Вернуться в студию
    backToStudio() {
        this.currentLocation = null;
        this.currentType = null;
        this.uploadedPhoto = null;
        this.showWelcome();

        // Сбросить input
        const fileInput = document.getElementById('photoInput');
        if (fileInput) fileInput.value = '';
    }

    // --- TOUR LOGIC ---

    initTour() {
        const slidesContainer = document.getElementById('tour-slides');
        if (!slidesContainer) return;

        MESSAGES.tour.locations.forEach((loc, index) => {
            const slide = document.createElement('div');
            slide.className = `tour-slide ${index === 0 ? 'active' : ''}`;
            slide.innerHTML = `
                <div class="tour-image-container">
                    <img src="${loc.image}" class="tour-image" alt="${loc.name}">
                </div>
                <div class="tour-info">
                    <h3 class="tour-title">${loc.name}</h3>
                    <p class="tour-desc">${loc.description}</p>
                </div>
            `;
            slidesContainer.appendChild(slide);
        });
    }

    openTour() {
        document.getElementById('tour-modal').classList.add('active');
        this.currentSlide = 0;
        this.updateSlides();
    }

    closeTour() {
        document.getElementById('tour-modal').classList.remove('active');
    }

    nextSlide() {
        this.currentSlide = (this.currentSlide + 1) % MESSAGES.tour.locations.length;
        this.updateSlides();
    }

    prevSlide() {
        this.currentSlide = (this.currentSlide - 1 + MESSAGES.tour.locations.length) % MESSAGES.tour.locations.length;
        this.updateSlides();
    }

    updateSlides() {
        const slides = document.querySelectorAll('.tour-slide');
        slides.forEach((slide, index) => {
            if (index === this.currentSlide) {
                slide.classList.add('active');
            } else {
                slide.classList.remove('active');
            }
        });
    }
}

// Инициализация при загрузке страницы
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new PhotoStudioApp();
});
