<template>

		<div class="viewForm" >
			
		<Input v-model='email' type="email" />

        <Input v-model='password' type="password" />
			
			
		</div>

</template>


<script >	
	export default {
		name: "viewForm",
		data() {
			return {
				email:"",
				password:"",
				
			}
		},
		methods: {
		}
	}
</script>

<style>

</style>