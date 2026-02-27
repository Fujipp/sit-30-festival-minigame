import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useGameStore = defineStore('game', () => {
    const currentLevel = ref(1)
    const currentQuestions = ref([])
    const activeQuestionIndex = ref(0)

    const activeQuestion = computed(
        () => currentQuestions.value[activeQuestionIndex.value] ?? {}
    )

    function selectLevel(level, questionsData) {
        currentLevel.value = level
        const levelKey = `level${level}`
        const sourceQuestions = questionsData[levelKey] ?? []

        currentQuestions.value = sourceQuestions.map((q) => ({ ...q }))
        activeQuestionIndex.value = 0
    }

    function openQuestion(index) {
        if (index < 0 || index >= currentQuestions.value.length) return
        activeQuestionIndex.value = index
    }

    return {
        currentLevel,
        currentQuestions,
        activeQuestionIndex,
        activeQuestion,
        selectLevel,
        openQuestion,
    }
})
