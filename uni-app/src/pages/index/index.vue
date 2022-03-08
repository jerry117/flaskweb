<template>
	<view class="content">
		<image class="logo" src="/static/logo.png"></image>
		<view>
			<text class="title">{{title}}</text>
		</view>
		<view class="button" >
			<button class="btn" @click="jumpPage">个人中心</button>
			
		</view>
		<div id="app"  v-cloak >
			<!-- {{greeting}} -->
			<view-form />
			<input @keyup.enter="greet" v-model="greeting"/>
			<hr />
			<!-- <button v-on:click="isVisible=! isVisible">Toggle box</button> -->
			<!-- 相同的写法 -->
			<!-- <button @click="isVisible=! isVisible">Toggle box</button> -->
			<div v-if="isVisible" class="box"></div>
			<button @click="togglebox">Toggle box</button>
		</div>
	</view>
</template>

<script >
	import {viewForm} from "./components/viewForm"
	export default {
		name: "index",
		components:{
			viewForm
		},
		data() {
			return {
				title: '首页',
				greeting: 'jerry',
				isVisible: false
			}
		},
		onLoad() {

		},
		methods: {
			jumpPage(){
				uni.navigateTo({
					url: '/pages/login/index'
				})
			},
			togglebox(){
				this.isVisible = ! this.isVisible
			},
			greet(){
				console.log(this.greeting)
			}


		}
	}
	
</script>

<style>
	.content {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
	}

	.logo {
		height: 200rpx;
		width: 200rpx;
		margin: 200rpx auto 50rpx auto;
	}

	.text-area {
		display: flex;
		justify-content: center;
	}

	.title {
		font-size: 36rpx;
		color: #8f8f94;
	}
	.button {
		color: red;
		/* background-color: yellow; */
	}
	.btn {
		/* color: red; */
		/* background-color: red; */
		color: black;
		display: block;
		margin: 200rpx
	}
	.box {
		background-color:purple;
		height: 200rpx;
		width: 200rpx;
	}
	[v-cloak]{
		display: none;

	}
</style>
