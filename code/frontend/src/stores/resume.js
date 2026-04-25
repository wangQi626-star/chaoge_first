import { defineStore } from 'pinia'
import api from '@/api'

export const useResumeStore = defineStore('resume', {
  state: () => ({
    currentResume: null,
    resumeData: {
      personal: {
        name: '',
        email: '',
        phone: '',
        position: '',
        photo: '',
        summary: ''
      },
      education: [],
      experience: [],
      projects: [],
      skills: []
    },
    selectedTemplate: null
  }),

  actions: {
    setTemplate(template) {
      this.selectedTemplate = template
    },

    updatePersonal(data) {
      this.resumeData.personal = { ...this.resumeData.personal, ...data }
    },

    addEducation(item) {
      this.resumeData.education.push(item)
    },

    updateEducation(index, item) {
      this.resumeData.education[index] = item
    },

    removeEducation(index) {
      this.resumeData.education.splice(index, 1)
    },

    addExperience(item) {
      this.resumeData.experience.push(item)
    },

    updateExperience(index, item) {
      this.resumeData.experience[index] = item
    },

    removeExperience(index) {
      this.resumeData.experience.splice(index, 1)
    },

    addProject(item) {
      this.resumeData.projects.push(item)
    },

    updateProject(index, item) {
      this.resumeData.projects[index] = item
    },

    removeProject(index) {
      this.resumeData.projects.splice(index, 1)
    },

    addSkill(skill) {
      if (skill && !this.resumeData.skills.includes(skill)) {
        this.resumeData.skills.push(skill)
      }
    },

    removeSkill(index) {
      this.resumeData.skills.splice(index, 1)
    },

    setResumeData(data) {
      this.resumeData = data
    },

    clearResumeData() {
      this.resumeData = {
        personal: { name: '', email: '', phone: '', position: '', photo: '', summary: '' },
        education: [],
        experience: [],
        projects: [],
        skills: []
      }
    },

    async saveResume(title, templateId) {
      const response = await api.post('/resumes/', {
        title,
        template: templateId,
        resume_data: this.resumeData
      })
      this.currentResume = response.data
      return response.data
    },

    async updateResume(resumeId) {
      const response = await api.patch(`/resumes/${resumeId}/`, {
        resume_data: this.resumeData
      })
      this.currentResume = response.data
      return response.data
    },

    async generatePdf(resumeId) {
      const response = await api.post(`/resumes/${resumeId}/generate_pdf/`)
      return response.data
    }
  }
})
