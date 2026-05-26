<script setup>
import axios from 'axios'

import {
  computed,
  onMounted,
  ref
} from 'vue'


// ======================================
// STATE
// ======================================

const loading = ref(true)

const report = ref({

  total_students: 0,

  total_companies: 0,

  total_drives: 0,

  total_applications: 0,

  applied: 0,

  shortlisted: 0,

  selected: 0,

  rejected: 0

})

const topCompanies = ref([])

const activities = ref([])


// ======================================
// FETCH REPORTS
// ======================================

const fetchReports = async () => {

  try {

    loading.value = true

    const token = localStorage.getItem('token')

    const headers = {

      Authorization: `Bearer ${token}`
    }


    // ======================================
    // REPORT SUMMARY
    // ======================================

    const reportResponse = await axios.get(
      'http://127.0.0.1:5000/api/admin/reports',
      { headers }
    )

    report.value = {

      total_students:
        reportResponse.data?.total_students || 0,

      total_companies:
        reportResponse.data?.total_companies || 0,

      total_drives:
        reportResponse.data?.total_drives || 0,

      total_applications:
        reportResponse.data?.total_applications || 0,

      applied:
        reportResponse.data?.applied || 0,

      shortlisted:
        reportResponse.data?.shortlisted || 0,

      selected:
        reportResponse.data?.selected || 0,

      rejected:
        reportResponse.data?.rejected || 0
    }


    // ======================================
    // TOP COMPANIES
    // ======================================

    try {

      const companiesResponse = await axios.get(
        'http://127.0.0.1:5000/api/admin/top-companies',
        { headers }
      )

      topCompanies.value =
        companiesResponse.data || []

    } catch (error) {

      console.log(
        'Top companies API error:',
        error
      )

      topCompanies.value = []
    }


    // ======================================
    // RECENT ACTIVITIES
    // ======================================

    try {

      const activitiesResponse = await axios.get(
        'http://127.0.0.1:5000/api/admin/activities',
        { headers }
      )

      activities.value =
        activitiesResponse.data || []

    } catch (error) {

      console.log(
        'Activities API error:',
        error
      )

      activities.value = []
    }

  } catch (error) {

    console.log(error)

    alert(
      error.response?.data?.message ||
      'Failed to load reports.'
    )

  } finally {

    loading.value = false
  }
}


// ======================================
// MOUNT
// ======================================

onMounted(() => {

  fetchReports()
})


// ======================================
// PLACEMENT RATIO
// ======================================

const placementRatio = computed(() => {

  if (!report.value.total_students) {

    return 0
  }

  return Math.round(

    (
      report.value.selected /
      report.value.total_students
    ) * 100
  )
})


// ======================================
// CIRCLE OFFSET
// ======================================

const progressOffset = computed(() => {

  return 440 - (

    (440 * placementRatio.value) / 100
  )
})


// ======================================
// EXPORT REPORT
// ======================================

const exportReport = async () => {

  try {

    const token = localStorage.getItem('token')

    const response = await axios.get(
      'http://127.0.0.1:5000/api/admin/export-report',
      {

        responseType: 'blob',

        headers: {

          Authorization: `Bearer ${token}`
        }
      }
    )

    const url = window.URL.createObjectURL(

      new Blob([response.data])
    )

    const link =
      document.createElement('a')

    link.href = url

    link.setAttribute(

      'download',
      'placement_report.csv'
    )

    document.body.appendChild(link)

    link.click()

    link.remove()

  } catch (error) {

    console.log(error)

    alert(

      error.response?.data?.message ||
      'Export Failed'
    )
  }
}
</script>