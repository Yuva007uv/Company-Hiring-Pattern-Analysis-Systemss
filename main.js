import Papa from 'papaparse';
import Chart from 'chart.js/auto';

// Global Data State
let rawData = [];
let companies = new Set();
let years = new Set();
let roles = new Set();
let skills = new Set();

// Chart Instances
let expChartInst = null;
let salChartInst = null;
let skillChartInst = null;

// DOM Elements
const companySelect = document.getElementById('companySelect');
const yearSelect = document.getElementById('yearSelect');
const roleSelect = document.getElementById('roleSelect');
const recSkillSelect = document.getElementById('recSkillSelect');
const topCompaniesList = document.getElementById('topCompaniesList');

// Chart Theme Styling
Chart.defaults.color = '#a1a1aa';
Chart.defaults.font.family = "'Inter', sans-serif";
const gridOptions = {
    color: 'rgba(255, 255, 255, 0.05)',
    tickColor: 'transparent',
    borderDash: [5, 5]
};

// Initialize app
async function init() {
    try {
        const response = await fetch('/company_data.csv');
        const csvText = await response.text();
        
        Papa.parse(csvText, {
            header: true,
            skipEmptyLines: true,
            complete: (results) => {
                rawData = results.data;
                extractUniqueValues();
                populateDropdowns();
                
                // Add event listeners
                companySelect.addEventListener('change', updateDashboard);
                yearSelect.addEventListener('change', updateDashboard);
                roleSelect.addEventListener('change', updateRecommendations);
                recSkillSelect.addEventListener('change', updateRecommendations);

                // Initial render JS triggers
                setTimeout(() => {
                    if (companies.size > 0 && years.size > 0) {
                        companySelect.value = Array.from(companies)[0];
                        yearSelect.value = Array.from(years)[0];
                        updateDashboard();
                    }
                }, 100);
            }
        });
    } catch (e) {
        console.error("Error loading data:", e);
    }
}

function extractUniqueValues() {
    rawData.forEach(row => {
        if(row.Company) companies.add(row.Company);
        if(row.Year) years.add(row.Year);
        if(row.Role) roles.add(row.Role);
        if(row.Skill) skills.add(row.Skill);
    });
}

function populateDropdowns() {
    const buildOptions = (set, el) => {
        el.innerHTML = '';
        Array.from(set).sort().forEach(val => {
            const opt = document.createElement('option');
            opt.value = val;
            opt.textContent = val;
            el.appendChild(opt);
        });
    };

    buildOptions(companies, companySelect);
    buildOptions(years, yearSelect);
    buildOptions(roles, roleSelect);
    buildOptions(skills, recSkillSelect);
    
    // Default recs
    roleSelect.value = Array.from(roles)[0];
    recSkillSelect.value = Array.from(skills)[0];
    updateRecommendations();
}

// Analytics Visualizations
function updateDashboard() {
    const activeCompany = companySelect.value;
    const activeYear = yearSelect.value;
    
    // Apply filtering
    const filtered = rawData.filter(d => d.Company === activeCompany && d.Year === activeYear);
    
    // Add animation class to charts container
    document.querySelectorAll('.chart-card').forEach(el => {
        el.style.opacity = '0';
        el.classList.remove('fade-in-up');
        void el.offsetWidth; // trigger reflow
        el.classList.add('fade-in-up');
    });

    renderExperienceChart(filtered);
    renderSalaryChart(filtered);
    renderSkillChart(filtered);
}

// Chart 1: Experience Distribution (Pie)
function renderExperienceChart(data) {
    const ctx = document.getElementById('experienceChart').getContext('2d');
    
    const counts = {};
    data.forEach(d => { counts[d.Experience] = (counts[d.Experience] || 0) + 1; });
    const labels = Object.keys(counts).map(v => v + ' Yrs');
    const values = Object.values(counts);

    if(expChartInst) expChartInst.destroy();
    
    expChartInst = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: ['#d4ff00', '#00f0ff', '#ff0055', '#bb86fc', '#03dac6'],
                borderColor: 'rgba(3,3,5,1)',
                borderWidth: 2,
                hoverOffset: 10
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '70%',
            plugins: {
                legend: { position: 'right', labels: { color: 'white', boxWidth: 12 } }
            }
        }
    });
}

// Chart 2: Salary by Role
function renderSalaryChart(data) {
    const ctx = document.getElementById('salaryChart').getContext('2d');
    
    // Group by Role, Average Salary
    const roleStats = {};
    data.forEach(d => {
        if(!roleStats[d.Role]) roleStats[d.Role] = {sum:0, count:0};
        roleStats[d.Role].sum += parseFloat(d.Salary_LPA);
        roleStats[d.Role].count += 1;
    });
    
    const labels = Object.keys(roleStats);
    const values = labels.map(r => (roleStats[r].sum / roleStats[r].count).toFixed(1));

    if(salChartInst) salChartInst.destroy();
    
    // Create gradient
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, '#00f0ff');
    gradient.addColorStop(1, 'rgba(0, 240, 255, 0.1)');

    salChartInst = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Avg Salary (LPA)',
                data: values,
                backgroundColor: gradient,
                borderRadius: 6,
                barThickness: 30
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { grid: gridOptions, beginAtZero: true },
                x: { grid: {display: false} }
            },
            plugins: { legend: { display: false } }
        }
    });
}

// Chart 3: Skill Demand
function renderSkillChart(data) {
    const ctx = document.getElementById('skillChart').getContext('2d');
    
    const counts = {};
    data.forEach(d => { counts[d.Skill] = (counts[d.Skill] || 0) + 1; });
    
    const labels = Object.keys(counts);
    const values = Object.values(counts);

    if(skillChartInst) skillChartInst.destroy();
    
    const gradient = ctx.createLinearGradient(0, 0, 400, 0);
    gradient.addColorStop(0, '#d4ff00');
    gradient.addColorStop(1, 'rgba(212, 255, 0, 0.2)');

    skillChartInst = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Demand Count',
                data: values,
                borderColor: '#d4ff00',
                backgroundColor: gradient,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: '#030305',
                pointBorderColor: '#d4ff00',
                pointBorderWidth: 2,
                pointRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { grid: gridOptions, beginAtZero: true },
                x: { grid: {display: false} }
            },
            plugins: { legend: { display: false } }
        }
    });
}

function updateRecommendations() {
    const targetRole = roleSelect.value;
    const targetSkill = recSkillSelect.value;
    
    const filtered = rawData.filter(d => d.Role === targetRole && d.Skill === targetSkill);
    
    const companyCount = {};
    filtered.forEach(d => {
        companyCount[d.Company] = (companyCount[d.Company] || 0) + 1;
    });
    
    // Sort top 3
    const sorted = Object.keys(companyCount).map(k => ({name: k, count: companyCount[k]}))
                         .sort((a,b) => b.count - a.count)
                         .slice(0, 3);
                         
    topCompaniesList.innerHTML = '';
    
    if(sorted.length === 0) {
        topCompaniesList.innerHTML = '<li>No exact matching openings found in dataset.</li>';
        return;
    }
    
    sorted.forEach(comp => {
        const li = document.createElement('li');
        li.innerHTML = `<span>${comp.name}</span> <span class="count">${comp.count} positions</span>`;
        topCompaniesList.appendChild(li);
    });
}

// Start app
document.addEventListener('DOMContentLoaded', init);
